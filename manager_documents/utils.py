import subprocess
import os

def convert_to_pdf(file_path, output_path):
    """
    Converte DOCX/DOC para PDF usando LibreOffice.
    """
    try:
        subprocess.run(
            ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(output_path), file_path],
            check=True
        )
        return output_path
    except subprocess.CalledProcessError:
        return None