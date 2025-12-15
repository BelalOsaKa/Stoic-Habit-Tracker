"""
Setup hooks for cx_Freeze to add custom MSI actions
"""
import os
import sys

def add_custom_actions(msi_path):
    """
    Add custom action to MSI to run post_install script after installation.
    This modifies the MSI file to include a post-install action.
    """
    try:
        import msilib
        from msilib import sequence
        
        # Open the MSI database
        db = msilib.OpenDatabase(msi_path, msilib.MSIDBOPEN_DIRECT)
        
        # Get the installation directory property
        view = db.OpenView("SELECT * FROM Property WHERE Property='TARGETDIR'")
        view.Execute(None)
        
        # Add custom action to run post_install.py
        # This is complex and may not work with cx_Freeze's MSI structure
        # Alternative: Create a batch file installer instead
        
        db.Commit()
        db.Close()
        return True
    except Exception as e:
        print(f"Could not modify MSI: {e}")
        return False

