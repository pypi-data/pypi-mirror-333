import json
import os
import tempfile
import urllib.request
import zipfile
import shutil
import logging
from pathlib import Path
import urllib.parse
import grp
import pwd

from tornado import web, ioloop
from jupyterhub.services.auth import HubOAuthenticated, HubOAuthCallbackHandler

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/srv/open_repo_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OpenRepoHandler(HubOAuthenticated, web.RequestHandler):
    # Note: Using HubOAuthenticated instead of HubAuthenticated
    # This class uses OAuth to authenticate users
    
    @web.authenticated
    async def get(self):
        logger.info(f"Authenticated user: {self.current_user}")
        
        # Get parameters from the request
        repo_url = self.get_argument('repo', None)
        notebook_path = self.get_argument('notebook', None)
        
        if not repo_url or not notebook_path:
            self.set_status(400)
            self.finish(json.dumps({
                "error": "Missing required parameters: repo and notebook"
            }))
            return
        
        try:
            # Create a temporary directory to store the repository
            with tempfile.TemporaryDirectory() as temp_dir:
                # Download the repository as a zip file
                zip_url = f"{repo_url}/archive/main.zip"
                if 'github.com' in repo_url:
                    # Convert GitHub URL to raw content URL
                    repo_parts = repo_url.split('github.com/')
                    if len(repo_parts) > 1:
                        owner_repo = repo_parts[1]
                        zip_url = f"https://github.com/{owner_repo}/archive/main.zip"
                
                logger.info(f"Downloading repository from: {zip_url}")
                zip_path = os.path.join(temp_dir, "repo.zip")
                urllib.request.urlretrieve(zip_url, zip_path)
                
                # Extract the zip file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find the notebook file
                extracted_dir = None
                for item in os.listdir(temp_dir):
                    if os.path.isdir(os.path.join(temp_dir, item)) and item != "repo.zip":
                        extracted_dir = os.path.join(temp_dir, item)
                        break
                
                if not extracted_dir:
                    self.set_status(404)
                    self.finish(json.dumps({
                        "error": "Could not extract repository"
                    }))
                    return
                
                notebook_file_path = os.path.join(extracted_dir, notebook_path)
                if not os.path.exists(notebook_file_path):
                    self.set_status(404)
                    self.finish(json.dumps({
                        "error": f"Notebook file {notebook_path} not found in repository"
                    }))
                    return
                
                # Copy the notebook to the user's workspace
                user = self.current_user
                username = user['name']
                logger.info(f"Processing for user: {username}")
                
                # Get the user's home directory
                # In JupyterHub, notebooks are typically stored in /home/{username}
                user_dir = f"/home/{username}"
                
                # Generate a unique filename to avoid collisions
                notebook_basename = os.path.basename(notebook_path)
                # Add repo name as prefix to avoid filename collisions
                repo_name = repo_url.split('/')[-1]
                unique_filename = f"{repo_name}_{notebook_basename}"
                
                # Copy the notebook file directly to user's home directory
                dest_path = os.path.join(user_dir, unique_filename)
                shutil.copy2(notebook_file_path, dest_path)
                logger.info(f"Copied notebook to: {dest_path}")
                
                # Set proper file permissions to ensure it's not read-only
                # rw-r--r-- permissions
                os.chmod(dest_path, 0o644)
                
                # Ensure both user and group permissions are set
                try:
                    # Get the primary group of the user
                    user_info = pwd.getpwnam(username)
                    group_name = grp.getgrgid(user_info.pw_gid).gr_name
                    
                    # Set user and group ownership
                    shutil.chown(dest_path, user=username, group=group_name)
                    logger.info(f"Set ownership for: {dest_path} to user: {username}, group: {group_name}")
                except Exception as e:
                    logger.warning(f"Could not change ownership: {str(e)}")
                
                logger.info(f"Set file permissions for: {dest_path}")

                # Use JupyterLab's URL parameters to open the notebook directly
                notebook_path_url = unique_filename
                
                # URL encode the path to handle special characters
                encoded_path = urllib.parse.quote(notebook_path_url)
                
                # Use JupyterLab's specific URL format to open the notebook directly
                # Format: /user/{username}/lab/tree/{path}
                redirect_url = f"/user/{username}/lab/tree/{encoded_path}"
                logger.info(f"Redirecting to: {redirect_url}")
                self.redirect(redirect_url)
                
        except Exception as e:
            logger.error(f"Error processing repository: {str(e)}", exc_info=True)
            self.set_status(500)
            self.finish(json.dumps({
                "error": f"Error processing repository: {str(e)}"
            }))

def main():
    # Get the service prefix from environment variable
    prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')
    
    # Make sure the prefix ends with a slash
    if not prefix.endswith('/'):
        prefix = prefix + '/'
    
    logger.info(f"Starting service with prefix: {prefix}")
    
    app = web.Application([
        (f"{prefix}", OpenRepoHandler),
        (f"{prefix}oauth_callback", HubOAuthCallbackHandler),
    ], cookie_secret=os.environ.get('JUPYTERHUB_API_TOKEN', 'secret'))
    
    port = int(os.environ.get('JUPYTERHUB_SERVICE_PORT', 8888))
    logger.info(f"Listening on port: {port}")
    app.listen(port)
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
