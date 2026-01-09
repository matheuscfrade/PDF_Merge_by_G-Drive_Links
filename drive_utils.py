import re
import gdown
import os

def extract_id_from_link(link):
    """
    Extracts the file or folder ID from a Google Drive link.
    """
    patterns = [
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'/folders/([a-zA-Z0-9_-]+)',
        r'id=([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
            
    if re.match(r'^[a-zA-Z0-9_-]+$', link):
        return link
        
    return None

def download_file(link, output_path):
    """
    Downloads a file from a public Google Drive link using gdown.
    """
    try:
        # Try to extract ID to make a robust download link
        file_id = extract_id_from_link(link)
        
        if file_id and len(file_id) > 10: # Simple length check for robustness
            # Construct direct download URL which gdown handles best
            final_url = f'https://drive.google.com/uc?id={file_id}'
            print(f"Extracted ID: {file_id}. Using URL: {final_url}")
        else:
            # Fallback to original link if ID extraction fails (e.g. specialized gdrive links)
            final_url = link
            print(f"Could not extract ID. Using original link: {final_url}")

        # gdown.download(url, output, quiet=False, fuzzy=True)
        out = gdown.download(final_url, output_path, quiet=True, fuzzy=True)
        
        if out and os.path.exists(out):
             # Verify it's not a small HTML error page (common with gdown/drive failures)
             if os.path.getsize(out) < 2000:
                  # Peek content to see if it's HTML
                  with open(out, 'rb') as f:
                      start = f.read(100)
                      if b'<!DOCTYPE html>' in start or b'<html' in start:
                          return False, "O arquivo parece ser privado ou não é um PDF válido. Verifique as permissões."
             
             return True, "Download realizado com sucesso."
        else:
             return False, "Falha no download. O link pode estar incorreto ou o arquivo não existe."
             
    except Exception as e:
        print(f"DEBUG Error: {str(e)}") # Log para o desenvolvedor
        return False, "Erro de conexão ou link inválido. Verifique se o link está correto."
