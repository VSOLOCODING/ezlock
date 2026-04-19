import os
import sys
import json
import base64
import getpass
import hashlib
import hmac
import time
import secrets
import string
import threading
import subprocess
import tempfile
import shutil
import atexit
import mmap
import queue
import webbrowser
import wave
import array
import math
import struct
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Try to import GUI libraries
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Try to import image preview
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Try to import video preview with optimized settings
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# Try to import PDF preview
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    try:
        import pdfplumber
        PDFPLUMBER_AVAILABLE = True
    except ImportError:
        PDFPLUMBER_AVAILABLE = False
    PYMUPDF_AVAILABLE = False

# Try to import audio playback
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Try to import audio processing
try:
    import pydub
    from pydub import AudioSegment
    from pydub.utils import make_chunks
    import pydub.effects
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

# Cryptography imports
from cryptography.hazmat.primitives import hashes, hmac as crypto_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import argon2
from argon2 import PasswordHasher

# ========== LICENSE INFORMATION ==========
MIT_LICENSE = """
MIT License

Copyright © 2026 Ezcool Entities. All rights reserved.
Ezlock V 1.0.0 is developed by Ezcode, a subsidiary of Ezcool Entities.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

SUPPORT_INFO = """
╔══════════════════════════════════════════════════════════════╗
║                 SUPPORT EZLOCK CREATOR                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  If you find EzLock useful, please consider supporting       ║
║  the developer with a small donation. Your support helps     ║
║  maintain and improve this software!                         ║
║                                                              ║
║  ┌────────────────────────────────────────────────────┐      ║
║  │  BITCOIN ADDRESS:                                  │      ║
║  │  bc1qm6pwqdrew7www4e92mahnf7rqwvmkhwrpyqjn5        │      ║
║  └────────────────────────────────────────────────────┘      ║
║                                                              ║
║                                                              ║ 
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
Your support will be appericated   (◑‿◐)
"""

USER_GUIDE = """
╔════════════════════════════════════════════════════════════╗
║                    EZLOCK USER GUIDE                       ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  QUICK START:                                              ║
║  ────────────────────────────────────────────────────────  ║
║  1. Create an account (register)                           ║
║  2. Login with your credentials                            ║
║  3. Select files or folders                                ║
║  4. Choose encryption method                               ║
║                                                            ║
║  ENCRYPTION TYPES:                                         ║
║  ────────────────────────────────────────────────────────  ║
║                                                            ║
║  [ACCOUNT ENCRYPTION]                                      ║
║  • Files are bound to your account                         ║
║  • Cannot be decrypted by others                           ║
║  • Uses your account password                              ║
║  • Best for personal files                                 ║
║                                                            ║
║  [PASSWORD ENCRYPTION]                                     ║
║  • Enter password in the bar                               ║
║  • Can be shared with anyone                               ║
║  • Best for sharing files                                  ║
║                                                            ║
║  FILE EXTENSIONS:                                          ║
║  ────────────────────────────────────────────────────────  ║
║                                                            ║
║  • Encrypted files: .ezlock                                ║
║  • Original file: secret.txt → secret.txt.ezlock           ║
║  • Random name: 9Xk2mP4qR.ezlock                           ║
║                                                            ║
║  STREAMING FORMATS (NEVER ENCRYPTED):                      ║
║  ────────────────────────────────────────────────────────  ║
║                                                            ║
║  • .m3u8, .m3u, .ts, .mpd, .m4s                            ║
║  • .ism, .isml, .hls, .dash, .smil                         ║
║  • .asx, .pls, .xspf, .strm                                ║
║                                                            ║
║  FOLDER SECURITY:                                          ║
║  ────────────────────────────────────────────────────────  ║
║                                                            ║
║  • Right-click a folder → "Secure Folder"                  ║
║  • New files are auto-encrypted                            ║
║  • Modified files are auto-encrypted                       ║
║  • Optional password protection                            ║
║  • Subfolder support available                             ║
║                                                            ║
║  SECURE EDIT:                                              ║
║  ────────────────────────────────────────────────────────  ║
║                                                            ║
║  • Double-click encrypted file                             ║
║  • Choose "Edit" from dialog                               ║
║  • File opens in default app                               ║
║  • Save changes - auto re-encrypted                        ║
║  • Cancel - changes discarded                              ║
║                                                            ║
║  CLI COMMANDS:                                             ║
║  ───────────────────────────────────────────────────────   ║
║                                                            ║
║  help              - Show help                             ║
║  gui               - Launch GUI mode                       ║
║  license           - Show MIT license                      ║
║  support           - Show support info (BTC address)       ║
║  guide             - Show this user guide                  ║
║  register          - Create new account                    ║
║  login             - Login to account                      ║
║  logout            - Logout current user                   ║
║  whoami            - Show current user                     ║
║  users             - List all users                        ║
║  ls                - List files                            ║
║  cd <folder>       - Change directory                      ║
║  pwd               - Show current directory                ║
║  enc <file>        - Encrypt file (account)                ║
║  enc -p <file>     - Encrypt with password                 ║
║  dec <file>        - Decrypt file (account)                ║
║  dec -p <file>     - Decrypt with password                 ║
║  secure <folder>   - Secure a folder                       ║
║  unsecure <folder> - Remove folder security                ║
║  folders           - List secure folders                   ║
║                                                            ║
║  GUI KEYBOARD SHORTCUTS:                                   ║
║  ────────────────────────────────────────────────────────  ║
║                                                            ║
║  Ctrl+A            - Select all                            ║
║  Ctrl+Shift+A      - Clear selection                       ║
║  Ctrl+E            - Encrypt (Account)                     ║
║  Ctrl+Shift+E      - Encrypt (Password) / Secure Edit      ║
║  Ctrl+D            - Decrypt (Account)                     ║
║  Ctrl+Shift+D      - Decrypt (Password)                    ║
║  Ctrl+Shift+F      - Secure current folder                 ║
║  Ctrl+P            - Preview                               ║
║  F5                - Refresh                               ║
║  Delete            - Delete                                ║
║                                                            ║
║  SECURITY NOTES:                                           ║
║  ────────────────────────────────────────────────────────  ║
║                                                            ║
║  • Lost passwords cannot be recovered!                     ║
║  • Always use strong passwords                             ║
║  • Preview is in-memory only (secure)                      ║
║  • Memory is wiped on exit                                 ║
║  • Temp files deleted on program close                     ║
║  • Streaming formats never encrypted                       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""


class SecureMemory:
    """Secure memory management - auto-wipes on exit"""
    
    def __init__(self):
        self._passwords = {}
        self._keys = {}
        self._metadata = {}
        atexit.register(self.wipe_all)
    
    def store_password(self, key, password):
        """Store password in memory"""
        self._passwords[key] = bytearray(password.encode())
    
    def get_password(self, key):
        """Get password from memory"""
        if key in self._passwords:
            return bytes(self._passwords[key]).decode()
        return None
    
    def store_key(self, key, key_data):
        """Store encryption key in memory"""
        self._keys[key] = bytearray(key_data)
    
    def get_key(self, key):
        """Get encryption key from memory"""
        if key in self._keys:
            return bytes(self._keys[key])
        return None
    
    def store_metadata(self, key, metadata):
        """Store metadata in memory"""
        self._metadata[key] = metadata
    
    def get_metadata(self, key):
        """Get metadata from memory"""
        return self._metadata.get(key)
    
    def wipe(self, key):
        """Wipe specific memory"""
        if key in self._passwords:
            for i in range(len(self._passwords[key])):
                self._passwords[key][i] = 0
            del self._passwords[key]
        
        if key in self._keys:
            for i in range(len(self._keys[key])):
                self._keys[key][i] = 0
            del self._keys[key]
        
        if key in self._metadata:
            del self._metadata[key]
    
    def wipe_all(self):
        """Wipe all sensitive data from memory"""
        for key in list(self._passwords.keys()):
            self.wipe(key)
        for key in list(self._keys.keys()):
            self.wipe(key)
        self._metadata.clear()


class SecureFolderHandler(FileSystemEventHandler):
    """Watchdog handler for auto-encrypt folders"""
    
    def __init__(self, core, folder_path, include_subfolders=True, password=None):
        self.core = core
        self.folder_path = folder_path
        self.include_subfolders = include_subfolders
        self.password = password
        self.is_running = True
        self.event_queue = queue.Queue()
        self.processing = False
        
    def on_created(self, event):
        """Handle file creation events"""
        if not self.is_running:
            return
            
        if event.is_directory:
            return
            
        filepath = event.src_path
        
        # Check if file is in watched folder (and subfolders if enabled)
        if not self.include_subfolders:
            if os.path.dirname(filepath) != self.folder_path:
                return
        
        # Don't encrypt already encrypted files
        if filepath.endswith('.ezlock'):
            return
        
        # Check if it's a streaming format (don't encrypt)
        streaming_formats = ['.m3u8', '.m3u', '.ts', '.mpd', '.m4s', '.ism', '.isml',
                            '.hls', '.dash', '.smil', '.asx', '.pls', '.xspf', '.strm']
        ext = os.path.splitext(filepath)[1].lower()
        if ext in streaming_formats:
            return
            
        # Add to queue for processing
        self.event_queue.put(('created', filepath))
        
        # Start processing thread if not already running
        if not self.processing:
            self.processing = True
            threading.Thread(target=self.process_events, daemon=True).start()
    
    def on_modified(self, event):
        """Handle file modification events"""
        if not self.is_running:
            return
            
        if event.is_directory:
            return
            
        filepath = event.src_path
        
        # Check if file is in watched folder (and subfolders if enabled)
        if not self.include_subfolders:
            if os.path.dirname(filepath) != self.folder_path:
                return
        
        # Don't encrypt already encrypted files
        if filepath.endswith('.ezlock'):
            return
        
        # Check if it's a streaming format (don't encrypt)
        streaming_formats = ['.m3u8', '.m3u', '.ts', '.mpd', '.m4s', '.ism', '.isml',
                            '.hls', '.dash', '.smil', '.asx', '.pls', '.xspf', '.strm']
        ext = os.path.splitext(filepath)[1].lower()
        if ext in streaming_formats:
            return
            
        # Add to queue for processing
        self.event_queue.put(('modified', filepath))
        
        # Start processing thread if not already running
        if not self.processing:
            self.processing = True
            threading.Thread(target=self.process_events, daemon=True).start()
    
    def process_events(self):
        """Process file events in background"""
        while self.is_running and not self.event_queue.empty():
            try:
                event_type, filepath = self.event_queue.get(timeout=1)
                
                # Wait a bit to ensure file is fully written
                time.sleep(0.5)
                
                if os.path.exists(filepath) and not filepath.endswith('.ezlock'):
                    # Encrypt the file
                    if self.password:
                        self.core.encrypt_file(filepath, password=self.password, random_name=False)
                    else:
                        self.core.encrypt_file(filepath, random_name=False)
                    
                    # Delete original if encryption succeeded
                    if os.path.exists(filepath + '.ezlock'):
                        try:
                            os.remove(filepath)
                        except:
                            pass
                            
            except queue.Empty:
                break
            except Exception as e:
                print(f"Error processing event: {e}")
        
        self.processing = False
    
    def stop(self):
        """Stop the handler"""
        self.is_running = False


class OptimizedVideoPlayer:
    """Optimized video player with smooth playback using direct frame display"""
    
    def __init__(self, preview_canvas, controls_callback=None):
        self.preview_canvas = preview_canvas
        self.controls_callback = controls_callback
        self.cap = None
        self.playing = False
        self.paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 0
        self.duration = 0
        self.update_job = None
        self.video_path = None
        self.fullscreen = False
        self.original_geometry = None
        self.root = None
        self.last_display_time = 0
        self.frame_interval = 33  # Default ~30fps
        self.playback_speed = 1.0
        self.target_fps = 30
        self.current_photo = None
        self.preview_width = 0
        self.preview_height = 0
        self.frame_buffer = None
        self.use_frame_buffer = True
        self.last_frame = None
        
    def set_root(self, root):
        """Set root window for fullscreen toggling"""
        self.root = root
    
    def load_video(self, filepath):
        """Load video file"""
        if not CV2_AVAILABLE:
            return False
        
        try:
            if self.cap:
                self.stop()
            
            self.cap = cv2.VideoCapture(filepath)
            if not self.cap.isOpened():
                return False
            
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            if self.fps <= 0:
                self.fps = 30
            
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            self.current_frame = 0
            self.video_path = filepath
            
            # Calculate frame interval based on target FPS
            self.target_fps = min(60, max(15, int(self.fps)))
            self.frame_interval = int(1000 / self.target_fps)
            
            # Get canvas dimensions
            self.preview_width = self.preview_canvas.winfo_width()
            self.preview_height = self.preview_canvas.winfo_height()
            if self.preview_width < 10:
                self.preview_width = 500
                self.preview_height = 400
            
            # Display first frame
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            return True
        except Exception as e:
            print(f"Video load error: {e}")
            return False
    
    def display_frame(self, frame):
        """Display video frame with proper scaling"""
        if not CV2_AVAILABLE or not self.preview_canvas:
            return
        
        try:
            # Get current canvas size
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width < 10:
                canvas_width = self.preview_width or 500
                canvas_height = self.preview_height or 400
            
            # Store for later use
            self.preview_width = canvas_width
            self.preview_height = canvas_height
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Calculate scaling ratio
            height, width = frame_rgb.shape[:2]
            ratio = min(canvas_width / width, canvas_height / height)
            
            # Only scale if needed (for performance)
            if ratio < 0.95 or ratio > 1.05:
                new_size = (int(width * ratio), int(height * ratio))
                frame_resized = cv2.resize(frame_rgb, new_size, interpolation=cv2.INTER_LINEAR)
            else:
                frame_resized = frame_rgb
            
            # Convert to PIL Image and then to PhotoImage
            image = Image.fromarray(frame_resized)
            photo = ImageTk.PhotoImage(image)
            
            # Store reference to prevent garbage collection
            self.current_photo = photo
            
            # Update canvas
            self.preview_canvas.delete('all')
            self.preview_canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=photo,
                anchor=tk.CENTER
            )
            
            # Callback for UI updates
            if self.controls_callback:
                self.controls_callback('frame_displayed', self.current_frame)
                
        except Exception as e:
            print(f"Frame display error: {e}")
    
    def play(self):
        """Start playback"""
        if not self.cap:
            return
        
        self.playing = True
        self.paused = False
        self.last_display_time = time.time()
        self.update()
    
    def pause(self):
        """Pause playback"""
        if self.playing:
            self.paused = not self.paused
            if not self.paused:
                self.last_display_time = time.time()
                self.update()
    
    def stop(self):
        """Stop playback"""
        self.playing = False
        self.paused = False
        
        if self.update_job and self.root:
            try:
                self.root.after_cancel(self.update_job)
            except:
                pass
            self.update_job = None
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.current_photo = None
    
    def seek(self, percentage):
        """Seek to position"""
        if not self.cap:
            return
        
        try:
            frame_num = int((percentage / 100) * self.total_frames)
            frame_num = max(0, min(frame_num, self.total_frames - 1))
            
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            self.current_frame = frame_num
            
            # Display frame at seek position
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
                # Reset position for continued playback
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                
                if self.controls_callback:
                    self.controls_callback('progress', percentage)
        except Exception as e:
            print(f"Seek error: {e}")
    
    def set_playback_speed(self, speed):
        """Set playback speed"""
        self.playback_speed = max(0.5, min(2.0, speed))
    
    def set_volume(self, volume):
        """Set volume (OpenCV doesn't support volume, this is for GUI compatibility)"""
        pass
    
    def toggle_fullscreen(self, root, preview_frame):
        """Toggle fullscreen mode"""
        if not root:
            return
        
        if not self.fullscreen:
            self.original_geometry = root.geometry()
            root.attributes('-fullscreen', True)
            self.fullscreen = True
        else:
            root.attributes('-fullscreen', False)
            if self.original_geometry:
                root.geometry(self.original_geometry)
            self.fullscreen = False
        
        # Refresh display after toggling fullscreen
        if self.cap and self.current_frame >= 0:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
    
    def update(self):
        """Smooth video playback with stable timing"""
        if not self.playing or self.paused or not self.cap:
            return

        ret, frame = self.cap.read()

        if ret:
            self.current_frame += 1
            self.display_frame(frame)

            # Proper FPS timing
            delay = int(1000 / self.fps) if self.fps > 0 else 33

            if self.controls_callback and self.total_frames > 0:
                percentage = (self.current_frame / self.total_frames) * 100
                self.controls_callback('progress', percentage)

            if self.root:
                self.update_job = self.root.after(delay, self.update)

        else:
            # Loop video
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.current_frame = 0
            if self.root:
                self.update_job = self.root.after(10, self.update)


class EzLockCore:
    """Core encryption engine - Shared between CLI and GUI"""
    
    def __init__(self):
        self.secure_mem = SecureMemory()
        self.user_db = '.users.vault'
        self.current_user = None
        self.master_key = None
        self.session_token = None
        self.current_dir = str(Path.home())
        self.temp_dir = None
        self.temp_files = []  # Track all temp files for cleanup on exit
        self.secure_folders = {}  # Dict of watched folders: {path: {'handler': handler, 'observer': observer, 'include_subfolders': bool, 'password': str}}
        self.editing_files = {}  # Dict of files being edited: {path: {'temp_path': str, 'original_path': str, 'password': str}}
        self.ph = PasswordHasher(
            time_cost=2,
            memory_cost=102400,
            parallelism=2,
            hash_len=32,
            salt_len=16
        )
        self.users = {}
        self.streaming_formats = [
            '.m3u8', '.m3u', '.ts', '.mpd', '.m4s', '.ism', '.isml',
            '.hls', '.dash', '.smil', '.asx', '.pls', '.xspf', '.strm'
        ]
        self.init_system()
    
    def init_system(self):
        """Initialize system"""
        self.system_id = self.generate_fingerprint()
        self.load_master_key()
        self.load_users()
        self.create_temp_dir()
        self.load_secure_folders()
        atexit.register(self.cleanup_all)
    
    def cleanup_all(self):
        """Cleanup everything on exit"""
        self.stop_all_folder_watchers()
        self.cleanup_all_temp_files()
        self.secure_mem.wipe_all()
    
    def create_temp_dir(self):
        """Create temporary directory for secure previews"""
        self.temp_dir = Path(tempfile.gettempdir()) / f"ezlock_{secrets.token_hex(4)}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def cleanup_temp_dir(self):
        """Clean up temporary directory - called on logout only"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def cleanup_all_temp_files(self):
        """Clean up ALL temporary files - called on program exit"""
        # Clean up tracked temp files
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        
        # Clean up temp directory
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def add_temp_file(self, filepath):
        """Add a temporary file to track for cleanup on exit"""
        if filepath not in self.temp_files:
            self.temp_files.append(filepath)
        return filepath
    
    def generate_fingerprint(self):
        """Generate system fingerprint"""
        try:
            hostname = os.environ.get('COMPUTERNAME') or os.environ.get('HOSTNAME') or 'unknown'
            if not hostname:
                hostname = os.uname().nodename if hasattr(os, 'uname') else 'unknown'
            home = os.path.expanduser('~')
            fingerprint = hashlib.sha3_256(
                f"{hostname}{home}{os.getuid() if hasattr(os, 'getuid') else '1000'}".encode()
            ).digest()
            return base64.b64encode(fingerprint).decode()
        except:
            return base64.b64encode(os.urandom(32)).decode()
    
    def load_master_key(self):
        """Load master encryption key"""
        key_file = '.ezlock.master'
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                encrypted_key = f.read()
            fingerprint_key = hashlib.sha3_256(self.system_id.encode()).digest()[:32]
            aesgcm = AESGCM(fingerprint_key)
            try:
                nonce = encrypted_key[:12]
                ciphertext = encrypted_key[12:]
                self.master_key = aesgcm.decrypt(nonce, ciphertext, None)
            except:
                print("[!] Master key corrupted, generating new one...")
                self.master_key = os.urandom(32)
        else:
            self.master_key = os.urandom(32)
            fingerprint_key = hashlib.sha3_256(self.system_id.encode()).digest()[:32]
            aesgcm = AESGCM(fingerprint_key)
            nonce = os.urandom(12)
            encrypted_key = nonce + aesgcm.encrypt(nonce, self.master_key, None)
            with open(key_file, 'wb') as f:
                f.write(encrypted_key)
            if os.name == 'posix':
                os.chmod(key_file, 0o600)
    
    def encrypt_vault(self, data):
        """Encrypt user vault with no headers"""
        nonce = os.urandom(12)
        aesgcm = AESGCM(self.master_key)
        timestamp = str(int(time.time())).encode()
        encrypted = aesgcm.encrypt(nonce, json.dumps(data).encode(), timestamp)
        return nonce + timestamp + encrypted
    
    def decrypt_vault(self, encrypted_data):
        """Decrypt user vault"""
        try:
            nonce = encrypted_data[:12]
            timestamp = encrypted_data[12:22]  # 10 bytes for timestamp
            ciphertext = encrypted_data[22:]
            aesgcm = AESGCM(self.master_key)
            decrypted = aesgcm.decrypt(nonce, ciphertext, timestamp)
            return json.loads(decrypted.decode())
        except Exception as e:
            print(f"[!] Failed to decrypt vault: {e}")
            return None
    
    def load_users(self):
        """Load users from vault"""
        if os.path.exists(self.user_db):
            try:
                with open(self.user_db, 'rb') as f:
                    encrypted_data = f.read()
                self.users = self.decrypt_vault(encrypted_data)
                if self.users is None:
                    print("[!] No users found, creating new user database...")
                    self.users = {}
            except Exception as e:
                print(f"[!] Error loading users: {e}")
                self.users = {}
        else:
            self.users = {}
    
    def save_users(self):
        """Save users to vault"""
        try:
            encrypted_data = self.encrypt_vault(self.users)
            
            temp_db = self.user_db + '.tmp'
            with open(temp_db, 'wb') as f:
                f.write(encrypted_data)
            
            if os.path.exists(self.user_db):
                os.remove(self.user_db)
            os.rename(temp_db, self.user_db)
            return True
        except Exception as e:
            print(f"[!] Failed to save users: {e}")
            return False
    
    def load_secure_folders(self):
        """Load secure folders from user data"""
        if self.current_user and self.current_user in self.users:
            user_data = self.users[self.current_user]
            if 'secure_folders' in user_data:
                for folder_data in user_data['secure_folders']:
                    path = folder_data.get('path')
                    include_subfolders = folder_data.get('include_subfolders', True)
                    password = folder_data.get('password')
                    if path and os.path.exists(path):
                        self.start_folder_watching(path, include_subfolders, password)
    
    def save_secure_folders(self):
        """Save secure folders to user data"""
        if self.current_user and self.current_user in self.users:
            folders = []
            for path, data in self.secure_folders.items():
                folders.append({
                    'path': path,
                    'include_subfolders': data.get('include_subfolders', True),
                    'password': data.get('password')
                })
            self.users[self.current_user]['secure_folders'] = folders
            self.save_users()
    
    def start_folder_watching(self, folder_path, include_subfolders=True, password=None):
        """Start watching a folder for auto-encryption"""
        try:
            from watchdog.observers import Observer
            
            folder_path = os.path.abspath(folder_path)
            
            if folder_path in self.secure_folders:
                return False, "[!] Folder already being watched"
            
            handler = SecureFolderHandler(self, folder_path, include_subfolders, password)
            observer = Observer()
            observer.schedule(handler, folder_path, recursive=include_subfolders)
            observer.start()
            
            self.secure_folders[folder_path] = {
                'handler': handler,
                'observer': observer,
                'include_subfolders': include_subfolders,
                'password': password,
                'start_time': time.time()
            }
            
            # Save to user data
            self.save_secure_folders()
            
            return True, f"[+] Now watching: {folder_path}"
            
        except ImportError:
            return False, "[-] watchdog module not installed. Run: pip install watchdog"
        except Exception as e:
            return False, f"[-] Error watching folder: {e}"
    
    def stop_folder_watching(self, folder_path):
        """Stop watching a folder"""
        if folder_path in self.secure_folders:
            try:
                data = self.secure_folders[folder_path]
                data['handler'].stop()
                data['observer'].stop()
                data['observer'].join(timeout=5)
                del self.secure_folders[folder_path]
                
                # Save to user data
                self.save_secure_folders()
                
                return True, f"[+] Stopped watching: {folder_path}"
            except Exception as e:
                return False, f"[-] Error stopping watcher: {e}"
        return False, "[!] Folder not found"
    
    def stop_all_folder_watchers(self):
        """Stop all folder watchers"""
        for folder_path in list(self.secure_folders.keys()):
            self.stop_folder_watching(folder_path)
    
    def get_secure_folders(self):
        """Get list of secure folders"""
        folders = []
        for path, data in self.secure_folders.items():
            folders.append({
                'path': path,
                'include_subfolders': data.get('include_subfolders', True),
                'has_password': data.get('password') is not None,
                'start_time': data.get('start_time', 0)
            })
        return folders
    
    def generate_random_filename(self, length=15):
        """Generate random filename with .ezlock extension"""
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length)) + '.ezlock'
    
    def _add_base64_padding(self, b64_string):
        """Add proper padding to base64 string"""
        padding = 4 - (len(b64_string) % 4)
        if padding != 4:
            b64_string += '=' * padding
        return b64_string
    
    def _extract_key_from_hash(self, hash_string):
        """Extract raw key from Argon2 hash and ensure proper padding"""
        # Argon2 hash format: $argon2id$v=19$m=102400,t=2,p=2$<salt>$<hash>
        parts = hash_string.split('$')
        if len(parts) < 6:
            raise ValueError("Invalid Argon2 hash format")
        
        # The hash part is the last element
        b64_hash = parts[-1]
        
        # Add padding if needed
        b64_hash = self._add_base64_padding(b64_hash)
        
        # Decode to bytes
        return base64.b64decode(b64_hash)
    
    def register(self, username, password):
        """Register new user"""
        if username in self.users:
            return False, "[-] Username already exists!"
        
        if len(password) < 8:
            return False, "[-] Password too short! Minimum 8 characters."
        
        try:
            # Generate salts
            encryption_salt = os.urandom(32)
            
            # Hash password with argon2 for authentication
            password_hash = self.ph.hash(password)
            
            # Derive user key using Argon2 for encryption
            ph = PasswordHasher(
                time_cost=2,
                memory_cost=102400,
                parallelism=2,
                hash_len=32,
                salt_len=32
            )
            user_master_key_hash = ph.hash(password, salt=encryption_salt)
            
            # Extract the raw key from the hash with proper padding
            user_master_key = self._extract_key_from_hash(user_master_key_hash)
            
            # Ensure we have exactly 32 bytes
            if len(user_master_key) != 32:
                user_master_key = user_master_key[:32] if len(user_master_key) > 32 else user_master_key.ljust(32, b'\0')
            
            # Create test verifier
            test_verifier = AESGCM(user_master_key)
            test_nonce = os.urandom(12)
            test_message = b"EzLock Verification"
            test_encrypted = test_verifier.encrypt(test_nonce, test_message, None)
            
            # Store user data
            self.users[username] = {
                'password_hash': password_hash,
                'encryption_salt': base64.b64encode(encryption_salt).decode(),
                'test_nonce': base64.b64encode(test_nonce).decode(),
                'test_encrypted': base64.b64encode(test_encrypted).decode(),
                'created': time.time(),
                'last_login': None,
                'failed_attempts': 0,
                'secure_folders': []  # Initialize empty secure folders list
            }
            
            if self.save_users():
                return True, "[+] Account created successfully!"
            else:
                return False, "[-] Failed to save user data!"
            
        except Exception as e:
            return False, f"[-] Registration failed: {e}"
    
    def login(self, username, password):
        """Login user"""
        if username not in self.users:
            return False, "[-] Username not found!"
        
        user_data = self.users[username]
        
        if user_data.get('failed_attempts', 0) >= 5:
            return False, "[-] Account locked after too many failed attempts. Restart app to retry."
        
        try:
            # Verify password with argon2
            self.ph.verify(user_data['password_hash'], password)
            
            # Derive user key using Argon2
            encryption_salt = base64.b64decode(user_data['encryption_salt'])
            ph = PasswordHasher(
                time_cost=2,
                memory_cost=102400,
                parallelism=2,
                hash_len=32,
                salt_len=32
            )
            user_master_key_hash = ph.hash(password, salt=encryption_salt)
            
            # Extract the raw key from the hash with proper padding
            user_master_key = self._extract_key_from_hash(user_master_key_hash)
            
            # Ensure we have exactly 32 bytes
            if len(user_master_key) != 32:
                user_master_key = user_master_key[:32] if len(user_master_key) > 32 else user_master_key.ljust(32, b'\0')
            
            # Verify key works
            test_nonce = base64.b64decode(user_data['test_nonce'])
            test_encrypted = base64.b64decode(user_data['test_encrypted'])
            test_verifier = AESGCM(user_master_key)
            test_decrypted = test_verifier.decrypt(test_nonce, test_encrypted, None)
            
            if test_decrypted != b"EzLock Verification":
                raise ValueError("Test verification failed")
            
            # Store key in secure memory
            self.secure_mem.store_key(f"user_{username}", user_master_key)
            self.current_user = username
            
            user_data['last_login'] = time.time()
            user_data['failed_attempts'] = 0
            self.save_users()
            
            self.session_token = secrets.token_hex(32)
            
            # Load secure folders
            self.load_secure_folders()
            
            return True, f"[+] Welcome back, {username}!"
            
        except argon2.exceptions.VerifyMismatchError:
            user_data['failed_attempts'] = user_data.get('failed_attempts', 0) + 1
            self.save_users()
            return False, "[-] Invalid password!"
        except Exception as e:
            user_data['failed_attempts'] = user_data.get('failed_attempts', 0) + 1
            self.save_users()
            return False, f"[-] Authentication failed: {e}"
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            # Stop all folder watchers
            self.stop_all_folder_watchers()
            
            # Wipe user key from memory
            self.secure_mem.wipe(f"user_{self.current_user}")
            self.current_user = None
        
        self.session_token = None
        return True, "[+] Logged out successfully!"
    
    def derive_key(self, password, salt=None):
        """Derive key from password using Argon2"""
        if salt is None:
            salt = os.urandom(32)
        else:
            salt = base64.b64decode(salt) if isinstance(salt, str) else salt
        
        ph = PasswordHasher(
            time_cost=2,
            memory_cost=102400,
            parallelism=2,
            hash_len=32,
            salt_len=32
        )
        key_hash = ph.hash(password, salt=salt)
        
        # Extract the raw key from the hash with proper padding
        key = self._extract_key_from_hash(key_hash)
        
        # Ensure we have exactly 32 bytes
        if len(key) != 32:
            key = key[:32] if len(key) > 32 else key.ljust(32, b'\0')
        
        return key, salt
    
    def encrypt_file(self, filepath, password=None, random_name=False, custom_name=None):
        """
        Encrypt file - produces raw encrypted data with NO headers
        Format: [12-byte nonce][32-byte salt][encrypted data][32-byte HMAC]
        Binary layout only — no readable headers
        Saved as .ezlock extension
        """
        if not self.current_user and not password:
            return False, "[-] Please login first or provide a password!"
        
        filepath = str(filepath)
        if not os.path.exists(filepath):
            return False, f"[-] File not found: {filepath}"
        
        # Don't encrypt already encrypted files
        if filepath.lower().endswith('.ezlock'):
            return False, "[-] File is already encrypted!"
        
        # Check for streaming formats - DON'T ENCRYPT
        ext = os.path.splitext(filepath)[1].lower()
        if ext in self.streaming_formats:
            return False, f"[-] Streaming format {ext} cannot be encrypted!"
        
        try:
            # Get encryption key
            if password:
                key, salt = self.derive_key(password)
                key_source = 'password'
            else:
                user_key = self.secure_mem.get_key(f"user_{self.current_user}")
                if not user_key:
                    return False, "[-] No user key found! Please login again."
                salt = os.urandom(32)
                # Derive file-specific key from user key using Argon2
                ph = PasswordHasher(
                    time_cost=1,
                    memory_cost=65536,
                    parallelism=1,
                    hash_len=32,
                    salt_len=32
                )
                # Use the user key as a password for deriving file key
                key_hash = ph.hash(base64.b64encode(user_key).decode(), salt=salt)
                key = self._extract_key_from_hash(key_hash)
                
                # Ensure we have exactly 32 bytes
                if len(key) != 32:
                    key = key[:32] if len(key) > 32 else key.ljust(32, b'\0')
                
                key_source = 'account'
            
            # Read file data
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            # Encrypt file data
            file_nonce = os.urandom(12)
            aesgcm = AESGCM(key)
            encrypted_data = aesgcm.encrypt(file_nonce, file_data, None)
            
            # Generate HMAC for integrity
            h = hmac.new(key, encrypted_data, hashlib.sha3_256)
            file_hmac = h.digest()
            
            # Final format: [nonce(12)][salt(32)][encrypted data][hmac(32)]
            final_data = file_nonce + salt + encrypted_data + file_hmac
            
            # Determine output filename with .ezlock extension
            if custom_name:
                encrypted_path = custom_name
                if not encrypted_path.endswith('.ezlock'):
                    encrypted_path += '.ezlock'
            elif random_name:
                name = self.generate_random_filename()
                encrypted_path = os.path.join(os.path.dirname(filepath), name)
            else:
                encrypted_path = filepath + '.ezlock'
            
            # Save encrypted file
            with open(encrypted_path, 'wb') as f:
                f.write(final_data)
            
            # Store metadata in memory only (never on disk)
            metadata = {
                'version': '1.0',
                'file_id': secrets.token_hex(16),
                'timestamp': time.time(),
                'original_name': os.path.basename(filepath),
                'original_size': len(file_data),
                'encryption': 'AES-256-GCM',
                'user': self.current_user if self.current_user else 'external',
                'key_source': key_source,
                'app_name': 'EzLock V 1.0.0',
                'app_version': '1.0.0'
            }
            
            # Encrypt metadata with a separate key and store in memory
            meta_key = hashlib.sha3_256(key + b"metadata").digest()
            meta_nonce = os.urandom(12)
            meta_aes = AESGCM(meta_key)
            meta_enc = meta_nonce + meta_aes.encrypt(meta_nonce, json.dumps(metadata).encode(), None)
            
            # Store in memory with file path as key
            self.secure_mem.store_key(f"meta_{encrypted_path}", meta_enc)
            
            if password:
                return True, f"[+] File encrypted with password: {encrypted_path}"
            else:
                return True, f"[+] File encrypted: {encrypted_path}"
            
        except Exception as e:
            return False, f"[-] Encryption failed: {e}"
    
    def decrypt_file(self, filepath, password=None, save_to_disk=True):
        """
        Decrypt file - expects raw format with no headers
        Format: [nonce(12)][salt(32)][encrypted data][hmac(32)]
        Expects .ezlock extension
        """
        filepath = str(filepath)
        if not os.path.exists(filepath):
            return False, f"[-] File not found: {filepath}", None
        
        if not filepath.endswith('.ezlock'):
            return False, "[-] Not an encrypted file! Expected .ezlock extension", None
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            if len(data) < 12 + 32 + 32:  # Minimum size
                return False, "[-] Invalid or corrupted file!", None
            
            # Extract components
            file_nonce = data[:12]
            salt = data[12:44]
            encrypted_data = data[44:-32]
            stored_hmac = data[-32:]
            
            decrypted_data = None
            metadata = None
            encryption_key = None
            key_source = None
            
            # Try account-based decryption first
            if self.current_user and not password:
                user_key = self.secure_mem.get_key(f"user_{self.current_user}")
                if user_key:
                    try:
                        # Derive file-specific key from user key using Argon2
                        ph = PasswordHasher(
                            time_cost=1,
                            memory_cost=65536,
                            parallelism=1,
                            hash_len=32,
                            salt_len=32
                        )
                        key_hash = ph.hash(base64.b64encode(user_key).decode(), salt=salt)
                        encryption_key = self._extract_key_from_hash(key_hash)
                        
                        # Ensure we have exactly 32 bytes
                        if len(encryption_key) != 32:
                            encryption_key = encryption_key[:32] if len(encryption_key) > 32 else encryption_key.ljust(32, b'\0')
                        
                        key_source = 'account'
                        
                        # Verify HMAC
                        h = hmac.new(encryption_key, encrypted_data, hashlib.sha3_256)
                        if hmac.compare_digest(h.digest(), stored_hmac):
                            # Decrypt
                            aesgcm = AESGCM(encryption_key)
                            decrypted_data = aesgcm.decrypt(file_nonce, encrypted_data, None)
                    except:
                        pass
            
            # Try password decryption
            if decrypted_data is None and password:
                try:
                    encryption_key, _ = self.derive_key(password, salt)
                    key_source = 'password'
                    
                    # Verify HMAC
                    h = hmac.new(encryption_key, encrypted_data, hashlib.sha3_256)
                    if hmac.compare_digest(h.digest(), stored_hmac):
                        # Decrypt
                        aesgcm = AESGCM(encryption_key)
                        decrypted_data = aesgcm.decrypt(file_nonce, encrypted_data, None)
                except:
                    pass
            
            if decrypted_data is None:
                return False, "[-] Decryption failed. Wrong password or file corrupted.", None
            
            # Try to get metadata from memory
            meta_enc = self.secure_mem.get_key(f"meta_{filepath}")
            if meta_enc:
                try:
                    meta_nonce = meta_enc[:12]
                    meta_cipher = meta_enc[12:]
                    meta_key = hashlib.sha3_256(encryption_key + b"metadata").digest()
                    meta_aes = AESGCM(meta_key)
                    meta_dec = meta_aes.decrypt(meta_nonce, meta_cipher, None)
                    metadata = json.loads(meta_dec.decode())
                except:
                    # Create basic metadata if stored one is corrupted
                    metadata = {
                        'original_name': os.path.basename(filepath).replace('.ezlock', ''),
                        'original_size': len(decrypted_data),
                        'key_source': key_source
                    }
            else:
                # Create basic metadata
                metadata = {
                    'original_name': os.path.basename(filepath).replace('.ezlock', ''),
                    'original_size': len(decrypted_data),
                    'key_source': key_source
                }
            
            if save_to_disk:
                original_name = metadata.get('original_name', 'decrypted_file')
                
                if os.path.exists(original_name):
                    base, ext = os.path.splitext(original_name)
                    original_name = f"{base}_decrypted{ext}"
                
                with open(original_name, 'wb') as f:
                    f.write(decrypted_data)
                
                return True, f"[+] File decrypted: {original_name}", (original_name, metadata)
            else:
                return True, "Decrypted in memory", (decrypted_data, metadata)
                
        except Exception as e:
            return False, f"[-] Decryption failed: {e}", None
    
    def secure_edit_start(self, filepath, password=None):
        """Start secure editing - decrypt to temp file"""
        if not filepath.endswith('.ezlock'):
            return False, "Not an encrypted file! Expected .ezlock extension", None
        
        # Try to decrypt with provided password or account
        success, message, data = self.decrypt_file(filepath, password, save_to_disk=False)
        
        if not success:
            return False, message, None
        
        decrypted_data, metadata = data
        
        # Create temp file for editing
        original_name = metadata.get('original_name', 'file')
        temp_filename = f"edit_{secrets.token_hex(8)}_{original_name}"
        temp_path = os.path.join(self.temp_dir, temp_filename)
        
        # Ensure temp directory exists
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        with open(temp_path, 'wb') as f:
            f.write(decrypted_data)
        
        # Track this temp file
        self.add_temp_file(temp_path)
        
        # Store editing info with the encryption key and metadata
        # Get the actual encryption key used for this file
        encryption_key = None
        if password:
            # For password-encrypted files, we need to derive the key again
            with open(filepath, 'rb') as f:
                data = f.read()
            salt = data[12:44]
            encryption_key, _ = self.derive_key(password, salt)
        else:
            # For account-encrypted files, get the user key and derive file key
            user_key = self.secure_mem.get_key(f"user_{self.current_user}")
            if user_key:
                with open(filepath, 'rb') as f:
                    data = f.read()
                salt = data[12:44]
                ph = PasswordHasher(
                    time_cost=1,
                    memory_cost=65536,
                    parallelism=1,
                    hash_len=32,
                    salt_len=32
                )
                key_hash = ph.hash(base64.b64encode(user_key).decode(), salt=salt)
                encryption_key = self._extract_key_from_hash(key_hash)
                if len(encryption_key) != 32:
                    encryption_key = encryption_key[:32] if len(encryption_key) > 32 else encryption_key.ljust(32, b'\0')
        
        self.editing_files[temp_path] = {
            'original_path': filepath,
            'password': password,
            'metadata': metadata,
            'start_time': time.time(),
            'encryption_key': encryption_key  # Store the key for re-encryption
        }
        
        return True, "Ready for editing", temp_path
    
    def secure_edit_save(self, temp_path):
        """Save edited file and re-encrypt"""
        if temp_path not in self.editing_files:
            return False, "No editing session found"
        
        edit_info = self.editing_files[temp_path]
        original_path = edit_info['original_path']
        password = edit_info['password']
        encryption_key = edit_info.get('encryption_key')
        metadata = edit_info.get('metadata', {})
        
        try:
            # Read edited file
            with open(temp_path, 'rb') as f:
                edited_data = f.read()
            
            # Get original file's salt and nonce to maintain compatibility
            with open(original_path, 'rb') as f:
                orig_data = f.read()
            
            if len(orig_data) < 12 + 32:
                return False, "Invalid original file format"
            
            file_nonce = orig_data[:12]
            salt = orig_data[12:44]
            
            # Determine which key to use for re-encryption
            if encryption_key is None:
                # Derive key again if not stored
                if password:
                    encryption_key, _ = self.derive_key(password, salt)
                else:
                    user_key = self.secure_mem.get_key(f"user_{self.current_user}")
                    if not user_key:
                        return False, "No user key found. Please login again."
                    ph = PasswordHasher(
                        time_cost=1,
                        memory_cost=65536,
                        parallelism=1,
                        hash_len=32,
                        salt_len=32
                    )
                    key_hash = ph.hash(base64.b64encode(user_key).decode(), salt=salt)
                    encryption_key = self._extract_key_from_hash(key_hash)
                    if len(encryption_key) != 32:
                        encryption_key = encryption_key[:32] if len(encryption_key) > 32 else encryption_key.ljust(32, b'\0')
            
            # Re-encrypt the edited data
            aesgcm = AESGCM(encryption_key)
            encrypted_data = aesgcm.encrypt(file_nonce, edited_data, None)
            
            # Generate new HMAC
            h = hmac.new(encryption_key, encrypted_data, hashlib.sha3_256)
            file_hmac = h.digest()
            
            # Final format: [nonce(12)][salt(32)][encrypted data][hmac(32)]
            final_data = file_nonce + salt + encrypted_data + file_hmac
            
            # Write the encrypted file
            with open(original_path, 'wb') as f:
                f.write(final_data)
            
            # Update metadata in memory
            meta_key = hashlib.sha3_256(encryption_key + b"metadata").digest()
            meta_nonce = os.urandom(12)
            meta_aes = AESGCM(meta_key)
            metadata['timestamp'] = time.time()
            metadata['original_size'] = len(edited_data)
            meta_enc = meta_nonce + meta_aes.encrypt(meta_nonce, json.dumps(metadata).encode(), None)
            self.secure_mem.store_key(f"meta_{original_path}", meta_enc)
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
            
            if temp_path in self.editing_files:
                del self.editing_files[temp_path]
            
            return True, "[+] File saved and re-encrypted"
        except Exception as e:
            return False, f"[-] Error saving: {e}"
    
    def secure_edit_cancel(self, temp_path):
        """Cancel editing - remove temp file"""
        if temp_path in self.editing_files:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                del self.editing_files[temp_path]
                return True, "Editing cancelled"
            except Exception as e:
                return False, f"Error: {e}"
        return False, "No editing session found"
    
    def preview_file(self, filepath, password=None):
        """Preview file content (for GUI) with metadata"""
        success, message, data = self.decrypt_file(filepath, password, save_to_disk=False)
        
        if not success:
            return False, message, None
        
        decrypted_data, metadata = data
        
        preview_info = {
            'data': decrypted_data,
            'metadata': metadata,
            'filename': os.path.basename(filepath),
            'original_name': metadata.get('original_name', 'unknown'),
            'size': len(decrypted_data),
            'type': self.get_file_type(decrypted_data),
            'key_source': metadata.get('key_source', 'unknown')
        }
        
        return True, "Preview ready", preview_info
    
    def get_file_type(self, data):
        """Determine file type from magic bytes"""
        if len(data) < 4:
            return 'text'
        
        signatures = {
            b'\x89PNG': ('image/png', 'IMAGE'),
            b'\xff\xd8\xff': ('image/jpeg', 'IMAGE'),
            b'GIF8': ('image/gif', 'IMAGE'),
            b'RIFF': ('image/webp', 'IMAGE'),
            b'%PDF': ('application/pdf', 'PDF'),
            b'PK': ('application/zip', 'ARCHIVE'),
            b'\x1f\x8b': ('application/gzip', 'ARCHIVE'),
            b'\x00\x00\x00\x18ftyp': ('video/mp4', 'VIDEO'),
            b'\x00\x00\x00\x1cftyp': ('video/mp4', 'VIDEO'),
            b'MOVI': ('video/quicktime', 'VIDEO'),
            b'ID3': ('audio/mpeg', 'AUDIO'),
            b'OggS': ('audio/ogg', 'AUDIO'),
        }
        
        for sig, (file_type, icon) in signatures.items():
            if data.startswith(sig):
                return file_type
        
        # Check for Office documents
        if data.startswith(b'PK\x03\x04'):
            if b'word/' in data[:1000]:
                return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif b'xl/' in data[:1000]:
                return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif b'ppt/' in data[:1000]:
                return 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            return 'application/zip'
        
        try:
            data.decode('utf-8')
            return 'text'
        except:
            return 'binary'
    
    def create_png_icon(self, icon_type, size=(16, 16)):
        """Create PNG icon programmatically"""
        if not PIL_AVAILABLE:
            return None
            
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        folder_color = (255, 193, 7, 255)  # Amber
        file_color = (33, 150, 243, 255)   # Blue
        enc_color = (156, 39, 176, 255)     # Purple
        image_color = (76, 175, 80, 255)    # Green
        video_color = (244, 67, 54, 255)    # Red
        audio_color = (255, 152, 0, 255)    # Orange
        pdf_color = (233, 30, 99, 255)       # Pink
        doc_color = (33, 150, 243, 255)      # Blue
        archive_color = (121, 85, 72, 255)   # Brown
        exe_color = (96, 125, 139, 255)      # Blue Grey
        text_color = (158, 158, 158, 255)    # Grey
        stream_color = (0, 188, 212, 255)    # Cyan
        ezlock_color = (156, 39, 176, 255)   # Purple for .ezlock files
        
        if icon_type == 'folder':
            # Folder icon
            draw.rectangle([2, 4, 14, 12], fill=folder_color, outline=None)
            draw.rectangle([4, 2, 12, 4], fill=folder_color, outline=None)
            draw.ellipse([7, 6, 9, 8], fill=(255, 255, 255, 255))
            
        elif icon_type == 'secure_folder':
            # Secure folder (with lock)
            draw.rectangle([2, 4, 14, 12], fill=folder_color, outline=None)
            draw.rectangle([4, 2, 12, 4], fill=folder_color, outline=None)
            draw.rectangle([6, 6, 10, 10], fill=(255, 255, 255, 255))
            draw.ellipse([7, 7, 9, 9], fill=(255, 0, 0, 255))
            
        elif icon_type == 'file':
            # Generic file
            draw.rectangle([3, 2, 13, 14], fill=file_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            
        elif icon_type == 'ezlock':
            # EzLock encrypted file (with lock and EZ text)
            draw.rectangle([3, 2, 13, 14], fill=ezlock_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.ellipse([6, 7, 10, 11], fill=(255, 255, 255, 255))
            draw.text((7, 8), "EZ", fill=ezlock_color, font=None)
            
        elif icon_type == 'image':
            # Image file
            draw.rectangle([3, 2, 13, 14], fill=image_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.ellipse([6, 7, 8, 9], fill=(255, 255, 255, 255))
            draw.rectangle([10, 10, 12, 12], fill=(255, 255, 255, 255))
            
        elif icon_type == 'video':
            # Video file
            draw.rectangle([3, 2, 13, 14], fill=video_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.polygon([7, 6, 11, 9, 7, 12], fill=(255, 255, 255, 255))
            
        elif icon_type == 'audio':
            # Audio file
            draw.rectangle([3, 2, 13, 14], fill=audio_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.arc([6, 6, 10, 12], start=0, end=180, fill=(255, 255, 255, 255), width=2)
            
        elif icon_type == 'pdf':
            # PDF file
            draw.rectangle([3, 2, 13, 14], fill=pdf_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.text((5, 6), "PDF", fill=(255, 255, 255, 255))
            
        elif icon_type == 'doc':
            # Document file
            draw.rectangle([3, 2, 13, 14], fill=doc_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.line([5, 6, 11, 6], fill=(255, 255, 255, 255), width=1)
            draw.line([5, 8, 11, 8], fill=(255, 255, 255, 255), width=1)
            draw.line([5, 10, 9, 10], fill=(255, 255, 255, 255), width=1)
            
        elif icon_type == 'archive':
            # Archive file
            draw.rectangle([3, 2, 13, 14], fill=archive_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.line([5, 6, 11, 12], fill=(255, 255, 255, 255), width=1)
            draw.line([11, 6, 5, 12], fill=(255, 255, 255, 255), width=1)
            
        elif icon_type == 'exe':
            # Executable file
            draw.rectangle([3, 2, 13, 14], fill=exe_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.text((6, 6), "EXE", fill=(255, 255, 255, 255))
            
        elif icon_type == 'text':
            # Text file
            draw.rectangle([3, 2, 13, 14], fill=text_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.line([5, 6, 11, 6], fill=(255, 255, 255, 255), width=1)
            draw.line([5, 8, 11, 8], fill=(255, 255, 255, 255), width=1)
            draw.line([5, 10, 11, 10], fill=(255, 255, 255, 255), width=1)
            
        elif icon_type == 'stream':
            # Streaming format
            draw.rectangle([3, 2, 13, 14], fill=stream_color, outline=None)
            draw.polygon([10, 2, 13, 5, 10, 5], fill=(255, 255, 255, 255))
            draw.line([6, 8, 10, 8], fill=(255, 255, 255, 255), width=2)
            draw.line([6, 10, 10, 10], fill=(255, 255, 255, 255), width=2)
            
        elif icon_type == 'parent':
            # Parent directory (up arrow)
            draw.rectangle([4, 8, 12, 12], fill=folder_color, outline=None)
            draw.polygon([6, 8, 10, 4, 14, 8], fill=folder_color, outline=None)
            
        return img
    
    def get_file_icon(self, filename, is_dir=False):
        """Get appropriate PNG icon for file"""
        if not PIL_AVAILABLE:
            return None
            
        if is_dir:
            if filename in self.secure_folders:
                return self.create_png_icon('secure_folder')
            return self.create_png_icon('folder')
        
        ext = os.path.splitext(filename)[1].lower()
        
        # Check for streaming formats first
        if ext in self.streaming_formats:
            return self.create_png_icon('stream')
        
        # Check for EzLock encrypted files
        if ext == '.ezlock':
            return self.create_png_icon('ezlock')
        
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', '.webp']:
            return self.create_png_icon('image')
        elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']:
            return self.create_png_icon('video')
        elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
            return self.create_png_icon('audio')
        elif ext in ['.pdf']:
            return self.create_png_icon('pdf')
        elif ext in ['.doc', '.docx']:
            return self.create_png_icon('doc')
        elif ext in ['.xls', '.xlsx']:
            return self.create_png_icon('doc')
        elif ext in ['.ppt', '.pptx']:
            return self.create_png_icon('doc')
        elif ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml']:
            return self.create_png_icon('text')
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return self.create_png_icon('archive')
        elif ext in ['.exe', '.msi', '.sh', '.bat']:
            return self.create_png_icon('exe')
        
        return self.create_png_icon('file')
    
    def save_preview_to_temp(self, data, filename):
        """Save preview data to temp file and track it"""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        temp_file = self.temp_dir / filename
        with open(temp_file, 'wb') as f:
            f.write(data)
        # Track this temp file for cleanup on exit
        return self.add_temp_file(str(temp_file))
    
    def list_files(self):
        """List files in current directory"""
        try:
            files = []
            path = Path(self.current_dir)
            
            for item in sorted(path.iterdir()):
                if item.is_dir():
                    # Check if this is a secure folder
                    is_secure = str(item) in self.secure_folders
                    icon = self.get_file_icon(item.name, is_dir=True)
                    files.append((icon, item.name, '', 'Folder', is_secure))
                else:
                    size = item.stat().st_size
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024**2:
                        size_str = f"{size/1024:.1f} KB"
                    elif size < 1024**3:
                        size_str = f"{size/1024**2:.1f} MB"
                    else:
                        size_str = f"{size/1024**3:.1f} GB"
                    
                    icon = self.get_file_icon(item.name)
                    
                    if item.suffix == '.ezlock':
                        file_type = 'EzLock Encrypted'
                    else:
                        ext = item.suffix.lower()
                        if ext in self.streaming_formats:
                            file_type = 'Streaming Format'
                        else:
                            file_type = 'File'
                    
                    files.append((icon, item.name, size_str, file_type, False))
            
            return True, files
        except Exception as e:
            return False, str(e)
    
    def format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def change_directory(self, folder):
        """Change current directory"""
        try:
            new_path = Path(self.current_dir) / folder
            if new_path.exists() and new_path.is_dir():
                self.current_dir = str(new_path.resolve())
                return True, f"[+] Changed to: {self.current_dir}"
            else:
                return False, "[-] Directory not found!"
        except Exception as e:
            return False, str(e)
    
    def get_current_directory(self):
        """Get current directory"""
        return self.current_dir
    
    def wipe_memory(self):
        """Wipe all sensitive data from memory"""
        self.secure_mem.wipe_all()
        return True, "[+] Memory wiped"
    
    def show_license(self):
        """Show MIT license"""
        return MIT_LICENSE
    
    def show_support(self):
        """Show support info with BTC address"""
        return SUPPORT_INFO
    
    def show_user_guide(self):
        """Show user guide"""
        return USER_GUIDE


class AudioPlayer:
    """Robust audio player with better error handling and stability"""

    def __init__(self):
        self.initialized = False
        self.loaded = False
        self.playing = False

        try:
            import pygame
            self.pg = pygame

            # Safer init (prevents crackling / device issues)
            self.pg.mixer.pre_init(44100, -16, 2, 512)
            self.pg.mixer.init()

            self.initialized = True
        except Exception as e:
            print("[Audio] Init failed:", e)
            self.initialized = False

    def load(self, filepath):
        """Load audio (safe)"""
        if not self.initialized:
            return False

        try:
            # Stop anything already playing
            self.stop()

            self.pg.mixer.music.load(filepath)
            self.loaded = True
            return True

        except Exception as e:
            print("[Audio] Load error:", e)
            self.loaded = False
            return False

    def play(self, loops=0):
        """Play audio"""
        if not (self.initialized and self.loaded):
            return

        try:
            self.pg.mixer.music.play(loops=loops)
            self.playing = True
        except Exception as e:
            print("[Audio] Play error:", e)

    def stop(self):
        """Stop audio safely"""
        if not self.initialized:
            return

        try:
            self.pg.mixer.music.stop()
            self.playing = False
        except:
            pass

    def pause(self):
        """Pause audio"""
        if self.initialized and self.playing:
            try:
                self.pg.mixer.music.pause()
            except:
                pass

    def resume(self):
        """Resume audio"""
        if self.initialized and self.loaded:
            try:
                self.pg.mixer.music.unpause()
            except:
                pass

    def set_volume(self, volume):
        """
        Set volume (0.0 → 1.0)
        """
        if self.initialized:
            try:
                volume = max(0.0, min(1.0, volume))
                self.pg.mixer.music.set_volume(volume)
            except:
                pass

    def is_busy(self):
        """Check if audio is still playing"""
        if self.initialized:
            return self.pg.mixer.music.get_busy()
        return False


class AudioAnalyzer:
    """Audio analysis for waveform and spectrum visualization"""
    
    @staticmethod
    def generate_waveform(filepath, points=500):
        """Generate accurate waveform from audio file"""
        if not PYDUB_AVAILABLE:
            return AudioAnalyzer._generate_simulated_waveform(filepath, points)
        
        try:
            # Load audio file
            audio = AudioSegment.from_file(filepath)
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Get raw samples
            samples = np.array(audio.get_array_of_samples())
            
            # Normalize to float between -1 and 1
            samples = samples / (2 ** (8 * audio.sample_width - 1))
            
            # Calculate chunk size for waveform
            chunk_size = max(1, len(samples) // points)
            
            # Generate waveform
            waveform = []
            for i in range(0, len(samples), chunk_size):
                chunk = samples[i:i+chunk_size]
                if len(chunk) > 0:
                    # Get peak amplitude for this chunk
                    peak = max(abs(np.max(chunk)), abs(np.min(chunk)))
                    waveform.append(peak)
            
            # Normalize waveform
            if waveform:
                max_val = max(waveform)
                if max_val > 0:
                    waveform = [w / max_val for w in waveform]
            
            return waveform
            
        except Exception as e:
            print(f"Waveform generation error: {e}")
            return AudioAnalyzer._generate_simulated_waveform(filepath, points)
    
    @staticmethod
    def _generate_simulated_waveform(filepath, points=500):
        """Generate simulated waveform when pydub is not available"""
        try:
            import wave
            if filepath.lower().endswith('.wav'):
                with wave.open(filepath, 'rb') as wav:
                    frames = wav.getnframes()
                    rate = wav.getframerate()
                    audio_data = wav.readframes(frames)
                    samples = array.array('h', audio_data)
                    
                    chunk_size = max(1, len(samples) // points)
                    waveform = []
                    for i in range(0, len(samples), chunk_size):
                        chunk = samples[i:i+chunk_size]
                        if chunk:
                            avg_amplitude = sum(abs(s) for s in chunk) / len(chunk)
                            waveform.append(avg_amplitude / 32768.0)
                    return waveform
        except:
            pass
        
        # Return sine-like simulated waveform
        return [abs(math.sin(i * math.pi / 50)) * 0.8 + 0.2 for i in range(points)]
    
    @staticmethod
    def compute_spectrum(audio_data, sample_rate, fft_size=2048):
        """Compute real-time frequency spectrum using FFT"""
        if not CV2_AVAILABLE:
            return []
        
        try:
            # Ensure we have enough data
            if len(audio_data) < fft_size:
                fft_size = len(audio_data)
            
            # Apply window function (Hanning)
            window = np.hanning(fft_size)
            windowed = audio_data[:fft_size] * window
            
            # Compute FFT
            fft = np.fft.rfft(windowed)
            magnitude = np.abs(fft)
            
            # Convert to dB scale
            magnitude_db = 20 * np.log10(magnitude + 1e-10)
            
            # Normalize
            magnitude_norm = (magnitude_db - np.min(magnitude_db)) / (np.max(magnitude_db) - np.min(magnitude_db) + 1e-10)
            
            # Reduce to reasonable number of bands (e.g., 64)
            bands = 64
            step = len(magnitude_norm) // bands
            spectrum = [np.mean(magnitude_norm[i:i+step]) for i in range(0, len(magnitude_norm), step)]
            spectrum = spectrum[:bands]
            
            # Create frequency bands (bass, mid, treble)
            bass = np.mean(spectrum[:bands//4]) if spectrum else 0
            mid = np.mean(spectrum[bands//4:bands//2]) if len(spectrum) > bands//4 else 0
            treble = np.mean(spectrum[bands//2:]) if len(spectrum) > bands//2 else 0
            
            return {
                'full': spectrum,
                'bass': bass,
                'mid': mid,
                'treble': treble
            }
        except:
            return {'full': [], 'bass': 0, 'mid': 0, 'treble': 0}
    
    @staticmethod
    def get_audio_info(filepath):
        """Get audio file information"""
        if PYDUB_AVAILABLE:
            try:
                audio = AudioSegment.from_file(filepath)
                return {
                    'duration': audio.duration_seconds,
                    'channels': audio.channels,
                    'sample_width': audio.sample_width,
                    'frame_rate': audio.frame_rate,
                    'max_possible_amplitude': 2 ** (8 * audio.sample_width - 1)
                }
            except:
                pass
        
        # Fallback for WAV files
        if filepath.lower().endswith('.wav'):
            try:
                import wave
                with wave.open(filepath, 'rb') as wav:
                    frames = wav.getnframes()
                    rate = wav.getframerate()
                    duration = frames / rate
                    return {
                        'duration': duration,
                        'channels': wav.getnchannels(),
                        'sample_width': wav.getsampwidth(),
                        'frame_rate': rate,
                        'max_possible_amplitude': 2 ** (8 * wav.getsampwidth() - 1)
                    }
            except:
                pass
        
        # Fallback for MP3 and other formats using pygame
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                sound = pygame.mixer.Sound(filepath)
                duration = sound.get_length()
                return {
                    'duration': duration,
                    'channels': 2,
                    'sample_width': 2,
                    'frame_rate': 44100,
                    'max_possible_amplitude': 32768
                }
            except:
                pass
        
        # Default fallback
        return {
            'duration': 0,
            'channels': 2,
            'sample_width': 2,
            'frame_rate': 44100,
            'max_possible_amplitude': 32768
        }


class EzLockGUI:
    """GUI Interface with secure preview and folder security"""
    
    def __init__(self, core):
        self.core = core
        if not TKINTER_AVAILABLE:
            print("Tkinter not available! Using CLI mode.")
            return
        
        self.root = tk.Tk()
        self.root.title("EzLock V1.0.0 - Secure File Encryption")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_styles()
        
        self.preview_temp_files = []  # Track temp files for this GUI session
        self.selected_indices = set()
        self.last_selected_index = None
        self.filter_var = tk.StringVar(value="All Files")
        self.login_status = None  # Initialize login_status
        self.shared_password_var = tk.StringVar()
        
        # Settings variables
        self.instant_preview_var = tk.BooleanVar(value=True)
        self.confirm_before_delete_var = tk.BooleanVar(value=True)
        self.random_filename_var = tk.BooleanVar(value=False)
        self.show_hidden_files_var = tk.BooleanVar(value=False)
        self.theme_var = tk.StringVar(value="System")
        
        # Initialize pygame for audio
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            except:
                pass
        
        # Video player - use optimized version
        self.video_player = None
        
        # Audio variables
        self.audio_playing = False
        self.audio_paused = False
        self.audio_position = 0
        self.audio_duration = 0
        self.audio_update_job = None
        self.audio_file = None
        self.audio_stream = None
        self.audio_play_btn = None
        self.audio_pause_btn = None
        self.audio_stop_btn = None
        self.audio_timeline = None
        self.audio_time_label = None
        self.audio_volume_var = None
        self.audio_volume_slider = None
        self.audio_canvas = None
        self.audio_waveform = []
        self.audio_spectrum = []
        self.waveform_height = 80
        self.spectrum_height = 60
        self.audio_analyzer = AudioAnalyzer()
        self.audio_spectrum_canvas = None
        self.audio_data_buffer = None
        
        # PDF variables
        self.pdf_document = None
        self.pdf_page = 0
        self.pdf_total_pages = 0
        self.pdf_prev_btn = None
        self.pdf_next_btn = None
        self.pdf_page_label = None
        self.pdf_controls = None
        
        # Preview state
        self.current_preview_file = None
        self.current_preview_data = None
        self.current_preview_metadata = None
        self.current_preview_is_encrypted = False
        self.current_preview_temp_file = None
        self.current_editing_file = None
        
        # Icon cache
        self.icon_cache = {}
        
        if self.core.current_user:
            self.create_main_screen()
        else:
            self.create_login_screen()
    
    def get_cached_icon(self, icon_type):
        """Get cached PNG icon"""
        if icon_type in self.icon_cache:
            return self.icon_cache[icon_type]
        
        icon = self.core.create_png_icon(icon_type)
        if icon:
            photo = ImageTk.PhotoImage(icon)
            self.icon_cache[icon_type] = photo
            return photo
        return None
    
    def setup_styles(self):
        """Setup ttk styles with colors"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Accent.TButton', background='#4CAF50', foreground='white')
        style.map('Accent.TButton', background=[('active', '#45a049')])
        
        style.configure('Warning.TButton', background='#F44336', foreground='white')
        style.map('Warning.TButton', background=[('active', '#da190b')])
        
        style.configure('Info.TButton', background='#2196F3', foreground='white')
        style.map('Info.TButton', background=[('active', '#0b7dda')])
        
        style.configure('Secure.TButton', background='#9C27B0', foreground='white')
        style.map('Secure.TButton', background=[('active', '#7B1FA2')])
        
        style.configure('Treeview', background='#f9f9f9', foreground='black', rowheight=25)
        style.configure('Treeview.Heading', background='#e1e1e1', foreground='black', font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#347083')], foreground=[('selected', 'white')])
    
    def on_closing(self):
        """Handle window close - cleanup ALL temp files"""
        # Stop video if playing
        if self.video_player:
            self.video_player.stop()
        
        self.stop_audio()
        
        # Cancel any active editing
        if self.current_editing_file:
            self.core.secure_edit_cancel(self.current_editing_file)
        
        # Clean up GUI temp files
        for temp_file in self.preview_temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        
        # Clean up core temp files
        self.core.cleanup_all_temp_files()
        
        # Wipe memory
        self.core.wipe_memory()
        
        # Quit pygame
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.quit()
                pygame.quit()
            except:
                pass
        
        # Destroy window
        self.root.destroy()
    
    def create_login_screen(self):
        """Create login/register screen"""
        self.clear_screen()
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = tk.Frame(main_frame)
        title_frame.pack(pady=50)
        
        title = tk.Label(
            title_frame,
            text="EzLock V1.0.0",
            font=('Arial', 42, 'bold'),
            fg='#4CAF50'
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Secure File Encryption with Folder Security",
            font=('Arial', 16),
            fg='#666666'
        )
        subtitle.pack(pady=10)
        
        login_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        login_frame.pack(pady=30, ipadx=30, ipady=20)
        
        tk.Label(
            login_frame,
            text="Login to Your Account",
            font=('Arial', 18, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).pack(pady=15)
        
        tk.Label(
            login_frame,
            text="Username:",
            font=('Arial', 11),
            bg='#ffffff'
        ).pack(anchor=tk.W, padx=20, pady=(10, 0))
        
        self.login_username = tk.Entry(
            login_frame,
            width=30,
            font=('Arial', 11),
            bd=2,
            relief=tk.GROOVE
        )
        self.login_username.pack(padx=20, pady=5, ipady=3)
        self.login_username.focus()
        
        tk.Label(
            login_frame,
            text="Password:",
            font=('Arial', 11),
            bg='#ffffff'
        ).pack(anchor=tk.W, padx=20, pady=(10, 0))
        
        self.login_password = tk.Entry(
            login_frame,
            width=30,
            font=('Arial', 11),
            show="*",
            bd=2,
            relief=tk.GROOVE
        )
        self.login_password.pack(padx=20, pady=5, ipady=3)
        
        self.login_password.bind('<Return>', lambda e: self.do_login())
        
        button_frame = tk.Frame(login_frame, bg='#ffffff')
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(
            button_frame,
            text="Login",
            command=self.do_login,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        login_btn.pack(side=tk.LEFT, padx=5)
        
        register_btn = tk.Button(
            button_frame,
            text="Register",
            command=self.show_register,
            bg='#2196F3',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        register_btn.pack(side=tk.LEFT, padx=5)
        
        cli_btn = tk.Button(
            main_frame,
            text="Switch to CLI Mode",
            command=self.switch_to_cli,
            bg='#666666',
            fg='white',
            font=('Arial', 10),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        cli_btn.pack(pady=10)
        
        self.login_status = tk.Label(
            main_frame,
            text="",
            fg='red',
            font=('Arial', 10)
        )
        self.login_status.pack()
    
    def switch_to_cli(self):
        """Switch to CLI mode"""
        self.on_closing()
        cli = EzLockCLI(self.core)
        cli.run()
    
    def show_register(self):
        """Show registration dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Register New Account")
        dialog.geometry("600x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Create New Account",
            font=('Arial', 24, 'bold'),
            fg='#4CAF50'
        ).pack(pady=30)
        
        frame = tk.Frame(dialog, bg='#ffffff', relief=tk.RAISED, bd=2)
        frame.pack(padx=50, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text="Username:",
            font=('Arial', 11),
            bg='#ffffff'
        ).pack(anchor=tk.W, padx=30, pady=(20, 0))
        
        username_entry = tk.Entry(
            frame,
            width=25,
            font=('Arial', 11),
            bd=2,
            relief=tk.GROOVE
        )
        username_entry.pack(padx=30, pady=5, ipady=3)
        username_entry.focus()
        
        tk.Label(
            frame,
            text="Password:",
            font=('Arial', 11),
            bg='#ffffff'
        ).pack(anchor=tk.W, padx=30, pady=(15, 0))
        
        password_entry = tk.Entry(
            frame,
            width=25,
            font=('Arial', 11),
            show="*",
            bd=2,
            relief=tk.GROOVE
        )
        password_entry.pack(padx=30, pady=5, ipady=3)
        
        tk.Label(
            frame,
            text="Confirm Password:",
            font=('Arial', 11),
            bg='#ffffff'
        ).pack(anchor=tk.W, padx=30, pady=(15, 0))
        
        confirm_entry = tk.Entry(
            frame,
            width=25,
            font=('Arial', 11),
            show="*",
            bd=2,
            relief=tk.GROOVE
        )
        confirm_entry.pack(padx=30, pady=5, ipady=3)
        
        req_frame = tk.LabelFrame(
            frame,
            text="Password Requirements",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#333333'
        )
        req_frame.pack(padx=30, pady=15, fill=tk.X)
        
        req_text = """- Minimum 4 characters
- Longer passwords are stronger
- Use a mix of letters, numbers, and symbols"""
        
        tk.Label(
            req_frame,
            text=req_text,
            justify=tk.LEFT,
            bg='#ffffff',
            font=('Arial', 9)
        ).pack(padx=10, pady=10)
        
        def do_register():
            username = username_entry.get().strip()
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords don't match")
                return
            
            success, message = self.core.register(username, password)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.login_username.delete(0, tk.END)
                self.login_username.insert(0, username)
                self.login_password.delete(0, tk.END)
                self.login_password.insert(0, password)
            else:
                messagebox.showerror("Error", message)
        
        button_frame = tk.Frame(frame, bg='#ffffff')
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Create Account",
            command=do_register,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg='#F44336',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
    
    def do_login(self):
        """Perform login"""
        if not hasattr(self, 'login_status') or self.login_status is None:
            self.login_status = tk.Label(
                self.root,
                text="",
                fg='red',
                font=('Arial', 10)
            )
            self.login_status.pack()
        
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            self.login_status.config(text="Please enter username and password")
            return
        
        success, message = self.core.login(username, password)
        if success:
            self.create_main_screen()
        else:
            self.login_status.config(text=message)
            self.login_password.delete(0, tk.END)
    
    def create_main_screen(self):
        """Create main GUI screen"""
        self.clear_screen()
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Encrypt (Account)", command=self.encrypt_dialog, accelerator="Ctrl+E")
        file_menu.add_command(label="Encrypt (Password)", command=self.show_shared_encryption_dialog, accelerator="Ctrl+Shift+E")
        file_menu.add_command(label="Decrypt (Account)", command=self.decrypt_dialog, accelerator="Ctrl+D")
        file_menu.add_command(label="Decrypt (Password)", command=self.show_shared_decryption_dialog, accelerator="Ctrl+Shift+D")
        file_menu.add_command(label="Secure Edit", command=self.secure_edit_dialog, accelerator="Ctrl+Shift+E")
        file_menu.add_command(label="Preview", command=self.preview_dialog, accelerator="Ctrl+P")
        file_menu.add_separator()
        file_menu.add_command(label="Refresh", command=self.refresh_files, accelerator="F5")
        file_menu.add_command(label="Delete", command=self.delete_selected, accelerator="Del")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Alt+F4")
        
        # Folder Security menu
        folder_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Folder Security", menu=folder_menu)
        folder_menu.add_command(label="Secure Current Folder", command=self.secure_current_folder)
        folder_menu.add_command(label="Add Secure Folder", command=self.add_secure_folder_dialog)
        folder_menu.add_command(label="Remove Secure Folder", command=self.remove_secure_folder_dialog)
        folder_menu.add_command(label="List Secure Folders", command=self.list_secure_folders)
        
        # Info menu
        info_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Info", menu=info_menu)
        info_menu.add_command(label="User Guide", command=self.show_user_guide_gui)
        info_menu.add_command(label="MIT License", command=self.show_license_gui)
        info_menu.add_command(label="Support Developer", command=self.show_support_gui)
        info_menu.add_separator()
        info_menu.add_command(label="About", command=self.show_about)
        
        # Select menu
        select_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Select", menu=select_menu)
        select_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        select_menu.add_command(label="Clear Selection", command=self.clear_selection, accelerator="Ctrl+Shift+A")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Secure Delete", command=self.secure_delete)
        tools_menu.add_command(label="Wipe Memory", command=self.wipe_memory)
        tools_menu.add_separator()
        tools_menu.add_command(label="Open Terminal", command=self.open_terminal)
        tools_menu.add_command(label="Switch to CLI", command=self.switch_to_cli)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Open Settings", command=self.show_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Commands", command=self.show_commands)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-e>', lambda e: self.encrypt_dialog())
        self.root.bind('<Control-E>', lambda e: self.encrypt_dialog())
        self.root.bind('<Control-d>', lambda e: self.decrypt_dialog())
        self.root.bind('<Control-D>', lambda e: self.decrypt_dialog())
        self.root.bind('<Control-p>', lambda e: self.preview_dialog())
        self.root.bind('<Control-P>', lambda e: self.preview_dialog())
        self.root.bind('<Control-Shift-E>', lambda e: self.secure_edit_dialog())
        self.root.bind('<Control-Shift-D>', lambda e: self.show_shared_decryption_dialog())
        self.root.bind('<Control-Shift-F>', lambda e: self.secure_current_folder())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Control-A>', lambda e: self.select_all())
        self.root.bind('<Control-Shift-a>', lambda e: self.clear_selection())
        self.root.bind('<Control-Shift-A>', lambda e: self.clear_selection())
        self.root.bind('<F5>', lambda e: self.refresh_files())
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        
        # Main paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left frame - File Browser
        left_frame = ttk.LabelFrame(main_paned, text="File Browser", padding="5")
        main_paned.add(left_frame, weight=1)
        
        # Navigation bar
        nav_frame = ttk.Frame(left_frame)
        nav_frame.pack(fill=tk.X, pady=5)
        
        back_btn = tk.Button(
            nav_frame,
            text="<- Back",
            command=self.go_back,
            bg='#2196F3',
            fg='white',
            bd=0,
            padx=10,
            pady=3,
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT, padx=2)
        
        self.dir_label = tk.Label(
            nav_frame,
            text=self.core.current_dir,
            font=('Arial', 9),
            bg='#ffffff',
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.dir_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(
            nav_frame,
            text="Browse",
            command=self.browse_directory,
            bg='#4CAF50',
            fg='white',
            bd=0,
            padx=10,
            pady=3,
            cursor='hand2'
        )
        browse_btn.pack(side=tk.RIGHT, padx=2)
        
        refresh_btn = tk.Button(
            nav_frame,
            text="R",
            command=self.refresh_files,
            bg='#FF9800',
            fg='white',
            bd=0,
            padx=10,
            pady=3,
            cursor='hand2',
            width=3
        )
        refresh_btn.pack(side=tk.RIGHT, padx=2)
        
        secure_btn = tk.Button(
            nav_frame,
            text="Secure Folder",
            command=self.secure_current_folder,
            bg='#9C27B0',
            fg='white',
            bd=0,
            padx=10,
            pady=3,
            cursor='hand2'
        )
        secure_btn.pack(side=tk.RIGHT, padx=2)
        
        # Filter bar
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=2)
        
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=[
                "All Files",
                "Encrypted Files (.ezlock)",
                "Images",
                "Videos",
                "Audio",
                "PDFs",
                "Documents",
                "Archives",
                "Streaming"
            ],
            state="readonly",
            width=20
        )
        filter_combo.pack(side=tk.LEFT, padx=2)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_files())
        
        self.selection_label = ttk.Label(filter_frame, text="0 selected", foreground='blue')
        self.selection_label.pack(side=tk.RIGHT, padx=5)
        
        # File tree
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Name', 'Size', 'Modified', 'Type')
        self.file_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='tree headings',
            height=20,
            selectmode='extended'
        )
        
        self.file_tree.heading('#0', text='', anchor=tk.W)
        self.file_tree.heading('Name', text='Name', anchor=tk.W)
        self.file_tree.heading('Size', text='Size', anchor=tk.W)
        self.file_tree.heading('Modified', text='Modified', anchor=tk.W)
        self.file_tree.heading('Type', text='Type', anchor=tk.W)
        
        self.file_tree.column('#0', width=30)
        self.file_tree.column('Name', width=300)
        self.file_tree.column('Size', width=100)
        self.file_tree.column('Modified', width=150)
        self.file_tree.column('Type', width=120)
        
        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.file_tree.xview)
        self.file_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.file_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.file_tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        self.file_tree.bind('<Double-Button-1>', self.on_file_double_click)
        self.file_tree.bind('<Button-3>', self.show_context_menu)
        
        # Set custom icons for tree items
        self.file_tree.tag_configure('folder', image=self.get_cached_icon('folder'))
        self.file_tree.tag_configure('secure_folder', image=self.get_cached_icon('secure_folder'))
        self.file_tree.tag_configure('file', image=self.get_cached_icon('file'))
        self.file_tree.tag_configure('ezlock', image=self.get_cached_icon('ezlock'))
        self.file_tree.tag_configure('image', image=self.get_cached_icon('image'))
        self.file_tree.tag_configure('video', image=self.get_cached_icon('video'))
        self.file_tree.tag_configure('audio', image=self.get_cached_icon('audio'))
        self.file_tree.tag_configure('pdf', image=self.get_cached_icon('pdf'))
        self.file_tree.tag_configure('doc', image=self.get_cached_icon('doc'))
        self.file_tree.tag_configure('archive', image=self.get_cached_icon('archive'))
        self.file_tree.tag_configure('exe', image=self.get_cached_icon('exe'))
        self.file_tree.tag_configure('text', image=self.get_cached_icon('text'))
        self.file_tree.tag_configure('stream', image=self.get_cached_icon('stream'))
        self.file_tree.tag_configure('parent', image=self.get_cached_icon('parent'))
        
        # Context menu
        self.context_menu = tk.Menu(self.file_tree, tearoff=0)
        self.context_menu.add_command(label="Encrypt (Account)", command=self.encrypt_selected)
        self.context_menu.add_command(label="Encrypt (Password)", command=self.show_shared_encryption_dialog)
        self.context_menu.add_command(label="Decrypt (Account)", command=self.decrypt_selected)
        self.context_menu.add_command(label="Decrypt (Password)", command=self.show_shared_decryption_dialog)
        self.context_menu.add_command(label="Secure Edit", command=self.secure_edit_selected)
        self.context_menu.add_command(label="Preview", command=self.preview_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Secure Folder", command=self.secure_current_folder)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        self.context_menu.add_command(label="Properties", command=self.show_properties)
        
        # Right frame - Preview and Info
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # User info bar
        top_frame = ttk.Frame(right_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        user_card = tk.Frame(top_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        user_card.pack(fill=tk.X, pady=2)
        
        avatar_frame = tk.Frame(user_card, bg='#4CAF50', width=40, height=40)
        avatar_frame.pack(side=tk.LEFT, padx=10, pady=5)
        avatar_frame.pack_propagate(False)
        
        tk.Label(
            avatar_frame,
            text="U",
            bg='#4CAF50',
            fg='white',
            font=('Arial', 20)
        ).pack(expand=True)
        
        info_frame = tk.Frame(user_card, bg='#ffffff')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
        
        tk.Label(
            info_frame,
            text=f"{self.core.current_user}",
            font=('Arial', 14, 'bold'),
            bg='#ffffff',
            fg='#4CAF50'
        ).pack(anchor=tk.W)
        
        logout_btn = tk.Button(
            user_card,
            text="Logout",
            command=self.logout,
            bg='#F44336',
            fg='white',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            font=('Arial', 10, 'bold')
        )
        logout_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Quick actions
        self.action_frame = tk.Frame(top_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        self.action_frame.pack(fill=tk.X, pady=2)
        
        title_frame = tk.Frame(self.action_frame, bg='#ffffff')
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            title_frame,
            text="Quick Actions",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#333333'
        ).pack(side=tk.LEFT)
        
        self.action_buttons_frame = tk.Frame(self.action_frame, bg='#ffffff')
        self.action_buttons_frame.pack(padx=10, pady=10, fill=tk.X)
        
        # Password bar
        password_frame = tk.Frame(top_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        password_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            password_frame,
            text="Password:",
            font=('Arial', 10, 'bold'),
            bg='#ffffff',
            fg='#9C27B0'
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        self.shared_password_entry = tk.Entry(
            password_frame,
            textvariable=self.shared_password_var,
            width=30,
            font=('Arial', 10),
            show="*",
            bd=2,
            relief=tk.GROOVE
        )
        self.shared_password_entry.pack(side=tk.LEFT, padx=5, pady=5, ipady=2)
        
        toggle_btn = tk.Button(
            password_frame,
            text="Show",
            command=self.toggle_password_visibility,
            bg='#666666',
            fg='white',
            bd=0,
            padx=8,
            pady=2,
            cursor='hand2',
            font=('Arial', 9)
        )
        toggle_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = tk.Button(
            password_frame,
            text="Clear",
            command=lambda: self.shared_password_var.set(""),
            bg='#F44336',
            fg='white',
            bd=0,
            padx=10,
            pady=2,
            cursor='hand2',
            font=('Arial', 9)
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Secure folder indicator
        self.secure_indicator = tk.Label(
            password_frame,
            text="",
            font=('Arial', 9),
            fg='#9C27B0',
            bg='#ffffff'
        )
        self.secure_indicator.pack(side=tk.RIGHT, padx=10)
        
        # Preview area
        preview_frame = ttk.LabelFrame(right_frame, text="Preview", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Preview mode selector
        mode_frame = ttk.Frame(preview_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mode_frame, text="View as:").pack(side=tk.LEFT, padx=5)
        
        self.preview_mode = tk.StringVar(value="auto")
        self.mode_combo = ttk.Combobox(
            mode_frame,
            textvariable=self.preview_mode,
            values=["auto", "original", "text", "hex"],
            state="readonly",
            width=15
        )
        self.mode_combo.pack(side=tk.LEFT, padx=5)
        self.mode_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_preview())
        
        self.preview_info_label = tk.Label(
            mode_frame,
            text="",
            font=('Arial', 9, 'italic'),
            fg='#666666'
        )
        self.preview_info_label.pack(side=tk.RIGHT, padx=10)
        
        # Main preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, bg='#f0f0f0', highlightthickness=1, highlightbackground='#cccccc')
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Text preview
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#ffffff',
            fg='black',
            height=10
        )
        
        # Create optimized video player
        self.video_player = OptimizedVideoPlayer(self.preview_canvas, self.video_controls_callback)
        self.video_player.set_root(self.root)
        
        # Video controls - create all widgets but pack later
        self.video_controls = tk.Frame(preview_frame, bg='#333333')
        
        # Top control row (timeline)
        top_control_row = tk.Frame(self.video_controls, bg='#333333')
        top_control_row.pack(fill=tk.X, padx=5, pady=2)
        
        # Timeline slider
        self.video_timeline = tk.Scale(
            top_control_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=400,
            bg='#333333',
            fg='white',
            highlightbackground='#666666',
            troughcolor='#555555',
            command=self.video_seek
        )
        self.video_timeline.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Time label
        self.video_time_label = tk.Label(
            top_control_row,
            text="00:00 / 00:00",
            bg='#333333',
            fg='white',
            font=('Arial', 9)
        )
        self.video_time_label.pack(side=tk.RIGHT, padx=5)
        
        # Bottom control row
        bottom_control_row = tk.Frame(self.video_controls, bg='#333333')
        bottom_control_row.pack(fill=tk.X, padx=5, pady=2)
        
        # Play/Pause/Stop buttons
        self.play_btn = tk.Button(
            bottom_control_row,
            text="▶",
            command=self.play_video,
            bg='#4CAF50',
            fg='white',
            bd=0,
            padx=15,
            pady=2,
            cursor='hand2',
            font=('Arial', 12, 'bold'),
            state=tk.DISABLED
        )
        self.play_btn.pack(side=tk.LEFT, padx=2)
        
        self.pause_btn = tk.Button(
            bottom_control_row,
            text="⏸",
            command=self.pause_video,
            bg='#FF9800',
            fg='white',
            bd=0,
            padx=15,
            pady=2,
            cursor='hand2',
            font=('Arial', 12, 'bold'),
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = tk.Button(
            bottom_control_row,
            text="⏹",
            command=self.stop_video,
            bg='#F44336',
            fg='white',
            bd=0,
            padx=15,
            pady=2,
            cursor='hand2',
            font=('Arial', 12, 'bold'),
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame rate control
        tk.Label(
            bottom_control_row,
            text="FPS:",
            bg='#333333',
            fg='white',
            font=('Arial', 9)
        ).pack(side=tk.LEFT, padx=(20, 2))
        
        self.fps_var = tk.StringVar(value="30")
        self.fps_combo = ttk.Combobox(
            bottom_control_row,
            textvariable=self.fps_var,
            values=["15", "24", "30", "60"],
            width=5,
            state="readonly"
        )
        self.fps_combo.pack(side=tk.LEFT, padx=2)
        self.fps_combo.bind('<<ComboboxSelected>>', self.on_fps_change)
        
        # Playback speed control
        tk.Label(
            bottom_control_row,
            text="Speed:",
            bg='#333333',
            fg='white',
            font=('Arial', 9)
        ).pack(side=tk.LEFT, padx=(20, 2))
        
        self.speed_var = tk.StringVar(value="1.0x")
        self.speed_combo = ttk.Combobox(
            bottom_control_row,
            textvariable=self.speed_var,
            values=["0.5x", "1.0x", "1.5x", "2.0x"],
            width=5,
            state="readonly"
        )
        self.speed_combo.pack(side=tk.LEFT, padx=2)
        self.speed_combo.bind('<<ComboboxSelected>>', self.on_speed_change)
        
        # Volume control
        tk.Label(
            bottom_control_row,
            text="🔊",
            bg='#333333',
            fg='white',
            font=('Arial', 10)
        ).pack(side=tk.LEFT, padx=(20, 2))
        
        self.volume_var = tk.IntVar(value=100)
        self.volume_slider = tk.Scale(
            bottom_control_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=100,
            variable=self.volume_var,
            bg='#333333',
            fg='white',
            highlightbackground='#666666',
            troughcolor='#555555',
            command=self.set_volume
        )
        self.volume_slider.pack(side=tk.LEFT, padx=2)
        
        # Fullscreen button
        self.fullscreen_btn = tk.Button(
            bottom_control_row,
            text="⛶ Fullscreen",
            command=self.toggle_fullscreen,
            bg='#2196F3',
            fg='white',
            bd=0,
            padx=15,
            pady=2,
            cursor='hand2',
            font=('Arial', 9, 'bold'),
            state=tk.DISABLED
        )
        self.fullscreen_btn.pack(side=tk.RIGHT, padx=2)
        
        # Audio controls with waveform and spectrum
        self.audio_controls = tk.Frame(preview_frame, bg='#333333')
        
        # Audio spectrum canvas (frequency visualization)
        spectrum_frame = tk.Frame(self.audio_controls, bg='#333333')
        spectrum_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(
            spectrum_frame,
            text="Frequency Spectrum",
            bg='#333333',
            fg='#00ff00',
            font=('Arial', 9, 'bold')
        ).pack(anchor=tk.W)
        
        self.audio_spectrum_canvas = tk.Canvas(
            spectrum_frame,
            height=self.spectrum_height,
            bg='#1a1a1a',
            highlightthickness=1,
            highlightbackground='#444444'
        )
        self.audio_spectrum_canvas.pack(fill=tk.X, pady=2)
        
        # Audio waveform canvas
        waveform_frame = tk.Frame(self.audio_controls, bg='#333333')
        waveform_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(
            waveform_frame,
            text="Waveform",
            bg='#333333',
            fg='#00ff00',
            font=('Arial', 9, 'bold')
        ).pack(anchor=tk.W)
        
        self.audio_canvas = tk.Canvas(
            waveform_frame,
            height=self.waveform_height,
            bg='#1a1a1a',
            highlightthickness=1,
            highlightbackground='#444444'
        )
        self.audio_canvas.pack(fill=tk.X, pady=2)
        
        # Audio top row (timeline)
        audio_top_row = tk.Frame(self.audio_controls, bg='#333333')
        audio_top_row.pack(fill=tk.X, padx=5, pady=2)
        
        # Audio timeline
        self.audio_timeline = tk.Scale(
            audio_top_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=400,
            bg='#333333',
            fg='white',
            highlightbackground='#666666',
            troughcolor='#555555',
            command=self.audio_seek
        )
        self.audio_timeline.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Audio time label
        self.audio_time_label = tk.Label(
            audio_top_row,
            text="00:00 / 00:00",
            bg='#333333',
            fg='white',
            font=('Arial', 9)
        )
        self.audio_time_label.pack(side=tk.RIGHT, padx=5)
        
        # Audio bottom row
        audio_bottom_row = tk.Frame(self.audio_controls, bg='#333333')
        audio_bottom_row.pack(fill=tk.X, padx=5, pady=2)
        
        # Audio play/pause/stop
        self.audio_play_btn = tk.Button(
            audio_bottom_row,
            text="▶",
            command=self.play_audio,
            bg='#4CAF50',
            fg='white',
            bd=0,
            padx=15,
            pady=2,
            cursor='hand2',
            font=('Arial', 12, 'bold'),
            state=tk.DISABLED
        )
        self.audio_play_btn.pack(side=tk.LEFT, padx=2)
        
        self.audio_pause_btn = tk.Button(
            audio_bottom_row,
            text="⏸",
            command=self.pause_audio,
            bg='#FF9800',
            fg='white',
            bd=0,
            padx=15,
            pady=2,
            cursor='hand2',
            font=('Arial', 12, 'bold'),
            state=tk.DISABLED
        )
        self.audio_pause_btn.pack(side=tk.LEFT, padx=2)
        
        self.audio_stop_btn = tk.Button(
            audio_bottom_row,
            text="⏹",
            command=self.stop_audio,
            bg='#F44336',
            fg='white',
            bd=0,
            padx=15,
            pady=2,
            cursor='hand2',
            font=('Arial', 12, 'bold'),
            state=tk.DISABLED
        )
        self.audio_stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Audio volume
        tk.Label(
            audio_bottom_row,
            text="🔊",
            bg='#333333',
            fg='white',
            font=('Arial', 10)
        ).pack(side=tk.LEFT, padx=(20, 2))
        
        self.audio_volume_var = tk.IntVar(value=100)
        self.audio_volume_slider = tk.Scale(
            audio_bottom_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=100,
            variable=self.audio_volume_var,
            bg='#333333',
            fg='white',
            highlightbackground='#666666',
            troughcolor='#555555',
            command=self.set_audio_volume
        )
        self.audio_volume_slider.pack(side=tk.LEFT, padx=2)
        
        # PDF controls
        self.pdf_controls = tk.Frame(preview_frame, bg='#333333')
        
        self.pdf_prev_btn = tk.Button(
            self.pdf_controls,
            text="Previous",
            command=self.pdf_prev_page,
            bg='#2196F3',
            fg='white',
            bd=0,
            padx=10,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.pdf_prev_btn.pack(side=tk.LEFT, padx=2)
        
        self.pdf_page_label = tk.Label(
            self.pdf_controls,
            text="Page 0/0",
            bg='#333333',
            fg='white',
            font=('Arial', 10)
        )
        self.pdf_page_label.pack(side=tk.LEFT, padx=10)
        
        self.pdf_next_btn = tk.Button(
            self.pdf_controls,
            text="Next",
            command=self.pdf_next_page,
            bg='#2196F3',
            fg='white',
            bd=0,
            padx=10,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.pdf_next_btn.pack(side=tk.LEFT, padx=2)
        
        # Preview buttons
        preview_buttons = tk.Frame(right_frame)
        preview_buttons.pack(fill=tk.X, pady=2)
        
        refresh_preview_btn = tk.Button(
            preview_buttons,
            text="Refresh Preview",
            command=self.refresh_preview,
            bg='#2196F3',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        refresh_preview_btn.pack(side=tk.LEFT, padx=2)
        
        clear_preview_btn = tk.Button(
            preview_buttons,
            text="Clear Preview",
            command=self.clear_preview,
            bg='#F44336',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        clear_preview_btn.pack(side=tk.LEFT, padx=2)
        
        save_preview_btn = tk.Button(
            preview_buttons,
            text="Save Decrypted",
            command=self.save_preview,
            bg='#4CAF50',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        save_preview_btn.pack(side=tk.RIGHT, padx=2)
        
        edit_btn = tk.Button(
            preview_buttons,
            text="Edit File",
            command=self.secure_edit_current,
            bg='#9C27B0',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        edit_btn.pack(side=tk.RIGHT, padx=2)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#e1e1e1',
            fg='#333333',
            padx=10,
            pady=2
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial file listing
        self.refresh_files()
        self.update_action_buttons()
        self.update_secure_indicator()
    
    def video_controls_callback(self, event, value=None):
        """Handle video player callbacks"""
        if event == 'progress' and value is not None:
            self.video_timeline.set(value)
        elif event == 'frame_displayed':
            if self.video_player and self.video_player.duration > 0:
                current_time = self.video_player.current_frame / self.video_player.fps if self.video_player.fps > 0 else 0
                minutes = int(current_time // 60)
                seconds = int(current_time % 60)
                total_minutes = int(self.video_player.duration // 60)
                total_seconds = int(self.video_player.duration % 60)
                self.video_time_label.config(text=f"{minutes:02d}:{seconds:02d} / {total_minutes:02d}:{total_seconds:02d}")
    
    def on_fps_change(self, event=None):
        """Handle FPS change"""
        if self.video_player:
            try:
                fps = int(self.fps_var.get())
                self.video_player.target_fps = fps
                self.video_player.frame_interval = int(1000 / fps)
            except:
                pass
    
    def on_speed_change(self, event=None):
        """Handle playback speed change"""
        if self.video_player:
            speed_str = self.speed_var.get()
            speed = float(speed_str.replace('x', ''))
            self.video_player.set_playback_speed(speed)
    
    def show_license_gui(self):
        """Show MIT license in a new window"""
        license_window = tk.Toplevel(self.root)
        license_window.title("EzLock - MIT License")
        license_window.geometry("600x500")
        license_window.transient(self.root)
        
        tk.Label(
            license_window,
            text="MIT License",
            font=('Arial', 18, 'bold'),
            fg='#4CAF50'
        ).pack(pady=10)
        
        text_frame = tk.Frame(license_window, bg='#ffffff', relief=tk.RAISED, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        text_widget = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#ffffff',
            fg='black',
            height=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_widget.insert('1.0', self.core.show_license())
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(
            license_window,
            text="Close",
            command=license_window.destroy,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=30,
            pady=8,
            cursor='hand2'
        ).pack(pady=10)
    
    def show_support_gui(self):
        """Show support info in a new window"""
        support_window = tk.Toplevel(self.root)
        support_window.title("EzLock - Support Developer")
        support_window.geometry("700x600")
        support_window.transient(self.root)
        
        tk.Label(
            support_window,
            text="Support EzLock Development",
            font=('Arial', 18, 'bold'),
            fg='#F7931A'
        ).pack(pady=10)
        
        main_frame = tk.Frame(support_window, bg='#ffffff', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            main_frame,
            text="If you find EzLock useful, please consider supporting\nthe developer with a small donation.",
            font=('Arial', 12),
            bg='#ffffff',
            fg='#333333',
            justify=tk.CENTER
        ).pack(pady=15)
        
        btc_frame = tk.Frame(main_frame, bg='#F7931A', width=100, height=100)
        btc_frame.pack(pady=10)
        btc_frame.pack_propagate(False)
        
        tk.Label(
            btc_frame,
            text="₿",
            font=('Arial', 48, 'bold'),
            bg='#F7931A',
            fg='white'
        ).pack(expand=True)
        
        btc_address = "bc1qm6pwqdrew7www4e92mahnf7rqwvmkhwrpyqjn5"
        
        addr_frame = tk.Frame(main_frame, bg='#f0f0f0', relief=tk.SUNKEN, bd=2)
        addr_frame.pack(padx=30, pady=15, fill=tk.X)
        
        tk.Label(
            addr_frame,
            text="Bitcoin Address:",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            fg='#F7931A'
        ).pack(pady=5)
        
        address_var = tk.StringVar(value=btc_address)
        addr_entry = tk.Entry(
            addr_frame,
            textvariable=address_var,
            width=50,
            font=('Courier', 11),
            bg='white',
            fg='black',
            state='readonly',
            justify=tk.CENTER
        )
        addr_entry.pack(padx=10, pady=5, ipady=5)
        
        def copy_address():
            support_window.clipboard_clear()
            support_window.clipboard_append(btc_address)
            messagebox.showinfo("Copied!", "Bitcoin address copied to clipboard!")
        
        tk.Button(
            main_frame,
            text="📋 Copy Address",
            command=copy_address,
            bg='#F7931A',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        ).pack(pady=10)
        
        qr_frame = tk.Frame(main_frame, bg='#f0f0f0', relief=tk.GROOVE, bd=2)
        qr_frame.pack(padx=30, pady=10, fill=tk.X)
        
        tk.Label(
            qr_frame,
            text="SCAN QR CODE",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#666666'
        ).pack(pady=10)
        
        qr_text = """
        
        
    █▀▀▀▀▀█  ▄ █ █▄▄▀▄███ ▄  ██ ▄██▄ ▄▀▄▄▄▄▄█ █▀▀▀▀▀█
    █ ███ █ █ ██▀▄  ▀█▄  ▀ ▀████▄  ▀ ▄▀▀▄▀ █▀ █ ███ █
    █ ▀▀▀ █  █▄▀▄█▀▄██  █▀█▀▀▀████ ▀ ▄▄▄▄█▄   █ ▀▀▀ █
    ▀▀▀▀▀▀▀ ▀▄█▄█▄▀ ▀▄▀▄█▄█ ▀ █▄▀ ▀▄▀▄█ █▄▀▄▀ ▀▀▀▀▀▀▀
     ▄▄█▀▄▀█▄▀▄  ▀▀▀ ▀▀█ █████▀▀▄█▄█▄██▀ ██▄█▄▄ ▄█▀▄▄
    ▄  ▄▄▄▀ ▄▄▀▀▀█▄  ██▄ █▀▄██ ▀ ▄██▀▀█   ▀▄▄▄▀ ▀▀▄▄█
    ▄▄█  █▀█▄ ▄▄█▄ █▄ █▀▀█▀▄▀ ▀▄▀▀▄█▀▀▀▀▀ ▄█ █▄ █  █
     █ █▀▀▀▄▀▄█ █▀▀▀▄▄   ▀▀▄▀█▀▀ █ ▄█▀▄ ▀▀█ ▀▄ ▀▄ █▄█
     ▄ █  ▀▀▄▀ █ █▀█ ▄ ▀  ▀ ▀▄▀▀ █▄▄█ ▄ ▀▀▀█ █▄█▀▀█▀▄
    ▄▄ ▄█ ▀    ▄ █   ▀▄▀█▄▄▀ ▀▀▄█ █   ▀▄▄ ▀█▄ ▄█▀█  ▀
    ▄ ▄█▀ ▀▀▄▄▄ ▀▄▄█▀ █ ▄█▀▄▀▀ █▀ █▀▄▄███▀██▄█▄ ▄▀▄▀▀
    ▀ █ █▀▀▀█▀▄ ███▀▀ ▀▄▀██▀▀▀█▄▀▄▀▀ ▄▄▀██ ▄█▀▀▀██▄ ▀
     ████ ▀ █▀▄▄█▄  ▄ ▄▄█ █ ▀ █▀▄▀█▄   ▄▀▄▄▄█ ▀ █ ▀█
    ▄██▄▀█▀█▀█▀█ █ █  ▄▀▄▄█▀▀▀█ █▄ ▄█▄▄▀█▄█▀▀▀▀███▄ ▀
    ▄██ ▀▀▀▄ ██▄▀█ ██▀ ██ ██ ▀ ▀██▄▀▀██▄▀█ ▀█▄█  █▄▄▀
    ▀█▀▄█▄▀█▀▀ ▄ ▀▀ ▀██ ▀▄▀█▀▀█▀▀▀▄▀█▀▀██ ▀▀█▄███▄ ▄█
     ▄  ▄ ▀ ▀▀▄▀  ▀▀█ ▀▄▀█▄ ▀ ▄▀█  █▄▄█▄█▀██▀ ▄▄█▄▀▀█
    ▄▄█▄▄▄▀▀█▀▄▀█▀▀▀█▄ ▀█▀██▀ ▄█▄▀▄▄███▀▀▀▄  ▄██▀▄▄ ▀
     ▄█ ▀ ▀█▄▄██▀▀▄  ▀ ▄█▄ ▀██ ██  █▀ ▀██▄▄█▀█▄ ████
     █▄▄ ▀▀▄▄▄▀██▄█ ▀▀█ ▄   █▄ ▀ ██▀ ▄ █▀█▀█▀██▀█▀▄▄█
    ▀▀▀   ▀ ▄▀██ ██▀▀█▄██ █▀▀▀█▀▄█▄▀██▀▀█▄▄██▀▀▀█ ▀ ▀
    █▀▀▀▀▀█ ▀ ▀█▀  ▄██  ▄▀█ ▀ █▀█▄▄██▀▀▄██▀▄█ ▀ █▄▀██
    █ ███ █ █ ▀▄▄█▀  ▀▀▄▄▄▀▀▀▀▀▄▄  ▄▄▄█▀▀██ ██▀▀█▄▄▀▄
    █ ▀▀▀ █  ▄█▀█▀▀  ▀▄█▀▄▀ ▄▀▄▄▀▀▄▀ █▄▀█▄▀▀▄▀██▀▄█▄█
    ▀▀▀▀▀▀▀   ▀ ▀   ▀ ▀▀ ▀▀▀ ▀      ▀▀▀ ▀  ▀▀▀    ▀ ▀
      
"""
        tk.Label(
            qr_frame,
            text=qr_text,
            font=('Courier', 8),
            bg='#f0f0f0',
            fg='black',
            justify=tk.CENTER
        ).pack(pady=5)
        
        tk.Label(
            main_frame,
            text="Thank you for your support! ❤️",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#4CAF50'
        ).pack(pady=15)
        
        tk.Button(
            support_window,
            text="Close",
            command=support_window.destroy,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=30,
            pady=8,
            cursor='hand2'
        ).pack(pady=10)
    
    def show_user_guide_gui(self):
        """Show user guide in a new window"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("EzLock - User Guide")
        guide_window.geometry("800x600")
        guide_window.transient(self.root)
        
        tk.Label(
            guide_window,
            text="EzLock V1.0.0 User Guide",
            font=('Arial', 18, 'bold'),
            fg='#4CAF50'
        ).pack(pady=10)
        
        text_frame = tk.Frame(guide_window, bg='#ffffff', relief=tk.RAISED, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        text_widget = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#ffffff',
            fg='black',
            height=30
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_widget.insert('1.0', self.core.show_user_guide())
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(
            guide_window,
            text="Close",
            command=guide_window.destroy,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=30,
            pady=8,
            cursor='hand2'
        ).pack(pady=10)
    
    def toggle_password_visibility(self):
        """Toggle shared password visibility"""
        if self.shared_password_entry.cget('show') == '*':
            self.shared_password_entry.config(show='')
            for widget in self.shared_password_entry.master.winfo_children():
                if isinstance(widget, tk.Button) and widget['text'] == 'Show':
                    widget.config(text='Hide')
        else:
            self.shared_password_entry.config(show='*')
            for widget in self.shared_password_entry.master.winfo_children():
                if isinstance(widget, tk.Button) and widget['text'] == 'Hide':
                    widget.config(text='Show')
    
    def update_secure_indicator(self):
        """Update secure folder indicator"""
        current = self.core.current_dir
        if current in self.core.secure_folders:
            data = self.core.secure_folders[current]
            sub = " + Subfolders" if data.get('include_subfolders', True) else ""
            pw = " (Password)" if data.get('password') else ""
            self.secure_indicator.config(text=f"[SECURE]{sub}{pw}")
        else:
            self.secure_indicator.config(text="")
    
    def secure_current_folder(self):
        """Secure the current folder"""
        current = self.core.current_dir
        
        if current in self.core.secure_folders:
            result = messagebox.askyesno(
                "Folder Already Secure",
                f"'{os.path.basename(current)}' is already a secure folder.\n\nRemove security from this folder?"
            )
            if result:
                success, message = self.core.stop_folder_watching(current)
                if success:
                    messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", message)
        else:
            dialog = tk.Toplevel(self.root)
            dialog.title("Secure Folder Options")
            dialog.geometry("500x400")
            dialog.transient(self.root)
            dialog.grab_set()
            
            tk.Label(
                dialog,
                text=f"Secure Folder: {os.path.basename(current)}",
                font=('Arial', 14, 'bold')
            ).pack(pady=20)
            
            frame = tk.Frame(dialog, bg='#ffffff', relief=tk.RAISED, bd=2)
            frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
            
            include_var = tk.BooleanVar(value=True)
            tk.Checkbutton(
                frame,
                text="Include subfolders (recursive)",
                variable=include_var,
                font=('Arial', 11),
                bg='#ffffff'
            ).pack(anchor=tk.W, padx=20, pady=10)
            
            use_password_var = tk.BooleanVar(value=False)
            tk.Checkbutton(
                frame,
                text="Use password protection",
                variable=use_password_var,
                font=('Arial', 11),
                bg='#ffffff',
                command=lambda: password_frame.pack(fill=tk.X, padx=20, pady=10) if use_password_var.get() else password_frame.pack_forget()
            ).pack(anchor=tk.W, padx=20, pady=10)
            
            password_frame = tk.Frame(frame, bg='#ffffff')
            
            tk.Label(
                password_frame,
                text="Password:",
                font=('Arial', 10),
                bg='#ffffff'
            ).pack(anchor=tk.W)
            
            password_entry = tk.Entry(
                password_frame,
                width=30,
                font=('Arial', 10),
                show="*",
                bd=2,
                relief=tk.GROOVE
            )
            password_entry.pack(pady=5, fill=tk.X)
            
            tk.Label(
                password_frame,
                text="Confirm:",
                font=('Arial', 10),
                bg='#ffffff'
            ).pack(anchor=tk.W)
            
            confirm_entry = tk.Entry(
                password_frame,
                width=30,
                font=('Arial', 10),
                show="*",
                bd=2,
                relief=tk.GROOVE
            )
            confirm_entry.pack(pady=5, fill=tk.X)
            
            info_label = tk.Label(
                frame,
                text="Files added or modified in this folder will be automatically encrypted.",
                font=('Arial', 9),
                fg='#666666',
                bg='#ffffff',
                wraplength=400
            )
            info_label.pack(padx=20, pady=20)
            
            def do_secure():
                password = None
                if use_password_var.get():
                    pw = password_entry.get()
                    confirm = confirm_entry.get()
                    if not pw:
                        messagebox.showerror("Error", "Please enter a password")
                        return
                    if pw != confirm:
                        messagebox.showerror("Error", "Passwords don't match")
                        return
                    password = pw
                
                success, message = self.core.start_folder_watching(
                    current,
                    include_subfolders=include_var.get(),
                    password=password
                )
                
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.refresh_files()
                    self.update_secure_indicator()
                else:
                    messagebox.showerror("Error", message)
            
            button_frame = tk.Frame(dialog)
            button_frame.pack(pady=20)
            
            tk.Button(
                button_frame,
                text="Secure Folder",
                command=do_secure,
                bg='#4CAF50',
                fg='white',
                font=('Arial', 11, 'bold'),
                bd=0,
                padx=20,
                pady=8,
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                button_frame,
                text="Cancel",
                command=dialog.destroy,
                bg='#F44336',
                fg='white',
                font=('Arial', 11, 'bold'),
                bd=0,
                padx=20,
                pady=8,
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=5)
    
    def add_secure_folder_dialog(self):
        """Add a secure folder manually"""
        folder = filedialog.askdirectory(
            title="Select Folder to Secure",
            initialdir=self.core.current_dir
        )
        
        if folder:
            if folder in self.core.secure_folders:
                messagebox.showinfo("Info", "Folder already secure")
                return
            
            self.core.current_dir = folder
            self.refresh_files()
            self.secure_current_folder()
    
    def remove_secure_folder_dialog(self):
        """Remove a secure folder"""
        folders = self.core.get_secure_folders()
        
        if not folders:
            messagebox.showinfo("Info", "No secure folders configured")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Remove Secure Folder")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Select folder to remove from security:",
            font=('Arial', 11)
        ).pack(pady=10)
        
        listbox = tk.Listbox(dialog, width=70, height=15)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        for folder in folders:
            sub = " (with subfolders)" if folder['include_subfolders'] else ""
            pw = " [Password]" if folder['has_password'] else ""
            listbox.insert(tk.END, f"{folder['path']}{sub}{pw}")
        
        def do_remove():
            selection = listbox.curselection()
            if not selection:
                messagebox.showinfo("Info", "Select a folder")
                return
            
            folder_path = folders[selection[0]]['path']
            success, message = self.core.stop_folder_watching(folder_path)
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_files()
                self.update_secure_indicator()
            else:
                messagebox.showerror("Error", message)
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Remove",
            command=do_remove,
            bg='#F44336',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg='#666666',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
    
    def list_secure_folders(self):
        """List all secure folders"""
        folders = self.core.get_secure_folders()
        
        if not folders:
            messagebox.showinfo("Secure Folders", "No secure folders configured")
            return
        
        msg = "SECURE FOLDERS\n"
        msg += "=" * 50 + "\n\n"
        
        for folder in folders:
            msg += f"[DIR] {folder['path']}\n"
            msg += f"   Include subfolders: {'Yes' if folder['include_subfolders'] else 'No'}\n"
            msg += f"   Password protected: {'Yes' if folder['has_password'] else 'No'}\n"
            msg += f"   Active since: {datetime.fromtimestamp(folder['start_time']).strftime('%Y-%m-%d %H:%M')}\n\n"
        
        messagebox.showinfo("Secure Folders", msg)
    
    def secure_edit_dialog(self):
        """Open file dialog for secure editing"""
        filepath = filedialog.askopenfilename(
            initialdir=self.core.current_dir,
            title="Select file to edit securely",
            filetypes=[("EzLock files", "*.ezlock"), ("All files", "*.*")]
        )
        if filepath:
            self.secure_edit_file(filepath)
    
    def secure_edit_selected(self):
        """Secure edit selected file"""
        files = self.get_selected_files()
        if not files:
            return
        
        filepath = files[0]
        if filepath.endswith('.ezlock'):
            self.secure_edit_file(filepath)
        else:
            messagebox.showinfo("Info", "Please select an encrypted file (.ezlock)")
    
    def secure_edit_current(self):
        """Secure edit currently previewed file"""
        if self.current_preview_file and self.current_preview_is_encrypted:
            self.secure_edit_file(self.current_preview_file)
    
    def secure_edit_file(self, filepath):
        """Start secure editing of a file"""
        password = None
        if filepath.endswith('.ezlock'):
            # Try to use password from password bar first
            if self.shared_password_var.get():
                password = self.shared_password_var.get()
            # If not logged in and no password in bar, ask for password
            elif not self.core.current_user:
                password = simpledialog.askstring(
                    "Password Required",
                    "Enter password for this file:",
                    show='*'
                )
                if password is None:
                    return
            # If logged in, we'll try account decryption first, then fall back to asking for password if fails
        
        success, message, temp_path = self.core.secure_edit_start(filepath, password)
        
        # If account decryption failed and user is logged in, ask for password
        if not success and self.core.current_user and "Wrong password" in message:
            password = simpledialog.askstring(
                "Password Required",
                "Account decryption failed. Enter password for this file (if password-encrypted):",
                show='*'
            )
            if password:
                success, message, temp_path = self.core.secure_edit_start(filepath, password)
        
        if not success:
            messagebox.showerror("Error", message)
            return
        
        self.current_editing_file = temp_path
        
        try:
            if sys.platform == 'win32':
                os.startfile(temp_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', temp_path]) 
            else:
                subprocess.run(['xdg-open', temp_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
            self.core.secure_edit_cancel(temp_path)
            return
        
        result = messagebox.askyesnocancel(
            "Editing Complete?",
            "Have you finished editing?\n\nYes - Save and re-encrypt\nNo - Continue editing\nCancel - Discard changes"
        )
        
        if result is True:
            success, message = self.core.secure_edit_save(temp_path)
            if success:
                messagebox.showinfo("Success", message)
                self.current_editing_file = None
                self.refresh_files()
            else:
                messagebox.showerror("Error", message)
        elif result is False:
            pass
        else:
            success, message = self.core.secure_edit_cancel(temp_path)
            if success:
                messagebox.showinfo("Info", message)
                self.current_editing_file = None
    
    def on_selection_change(self, event):
        """Handle selection change"""
        selected = self.file_tree.selection()
        self.selection_label.config(text=f"{len(selected)} selected")
        self.update_action_buttons()
        
        if self.instant_preview_var.get() and len(selected) == 1:
            self.preview_selected()
    
    def get_selected_files(self):
        """Get list of selected file paths"""
        files = []
        for item in self.file_tree.selection():
            values = self.file_tree.item(item)['values']
            if values and len(values) > 0:
                name = values[0]
                if name and name != '..':
                    file_path = str(Path(self.core.current_dir) / name)
                    if os.path.exists(file_path):
                        files.append(file_path)
        return files
    
    def select_all(self):
        """Select all files"""
        self.file_tree.selection_set(self.file_tree.get_children())
    
    def clear_selection(self):
        """Clear selection"""
        self.file_tree.selection_remove(self.file_tree.selection())
    
    def filter_file(self, filename, file_type):
        """Check if file matches current filter"""
        if not self.show_hidden_files_var.get() and filename.startswith('.'):
            return False
        
        filter_type = self.filter_var.get()
        
        if filter_type == "All Files":
            return True
        elif filter_type == "Encrypted Files (.ezlock)":
            return filename.endswith('.ezlock')
        elif filter_type == "Images":
            ext = os.path.splitext(filename)[1].lower()
            return ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', '.webp']
        elif filter_type == "Videos":
            ext = os.path.splitext(filename)[1].lower()
            return ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']
        elif filter_type == "Audio":
            ext = os.path.splitext(filename)[1].lower()
            return ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']
        elif filter_type == "PDFs":
            ext = os.path.splitext(filename)[1].lower()
            return ext in ['.pdf']
        elif filter_type == "Documents":
            ext = os.path.splitext(filename)[1].lower()
            return ext in ['.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.md']
        elif filter_type == "Archives":
            ext = os.path.splitext(filename)[1].lower()
            return ext in ['.zip', '.rar', '.7z', '.tar', '.gz']
        elif filter_type == "Streaming":
            ext = os.path.splitext(filename)[1].lower()
            return ext in self.core.streaming_formats
        
        return True
    
    def refresh_files(self):
        """Refresh file list"""
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        self.dir_label.config(text=self.core.current_dir)
        self.update_secure_indicator()
        
        current = Path(self.core.current_dir)
        if current.parent != current:
            parent_icon = self.get_cached_icon('parent')
            self.file_tree.insert('', 'end', image=parent_icon, values=('..', '', '', 'Parent Directory'), tags=('parent',))
        
        success, files = self.core.list_files()
        file_count = 0
        if success:
            for icon_img, name, size, ftype, is_secure in files:
                if not self.filter_file(name, ftype):
                    continue
                
                try:
                    file_path = Path(self.core.current_dir) / name
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    modified = mtime.strftime('%Y-%m-%d %H:%M')
                except:
                    modified = ''
                
                if is_secure:
                    tag = 'secure_folder'
                    icon = self.get_cached_icon('secure_folder')
                elif os.path.isdir(file_path):
                    tag = 'folder'
                    icon = self.get_cached_icon('folder')
                elif name.endswith('.ezlock'):
                    tag = 'ezlock'
                    icon = self.get_cached_icon('ezlock')
                else:
                    ext = os.path.splitext(name)[1].lower()
                    if ext in self.core.streaming_formats:
                        tag = 'stream'
                        icon = self.get_cached_icon('stream')
                    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', '.webp']:
                        tag = 'image'
                        icon = self.get_cached_icon('image')
                    elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']:
                        tag = 'video'
                        icon = self.get_cached_icon('video')
                    elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
                        tag = 'audio'
                        icon = self.get_cached_icon('audio')
                    elif ext in ['.pdf']:
                        tag = 'pdf'
                        icon = self.get_cached_icon('pdf')
                    elif ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                        tag = 'doc'
                        icon = self.get_cached_icon('doc')
                    elif ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml']:
                        tag = 'text'
                        icon = self.get_cached_icon('text')
                    elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
                        tag = 'archive'
                        icon = self.get_cached_icon('archive')
                    elif ext in ['.exe', '.msi', '.sh', '.bat']:
                        tag = 'exe'
                        icon = self.get_cached_icon('exe')
                    else:
                        tag = 'file'
                        icon = self.get_cached_icon('file')
                
                self.file_tree.insert('', 'end', image=icon, values=(name, size, modified, ftype), tags=(tag,))
                file_count += 1
        
        self.status_bar.config(text=f"[DIR] {file_count} files | User: {self.core.current_user} | .ezlock format")
        self.selection_label.config(text="0 selected")
        self.update_action_buttons()
    
    def show_context_menu(self, event):
        """Show context menu on right click"""
        try:
            item = self.file_tree.identify_row(event.y)
            if item:
                if item not in self.file_tree.selection():
                    self.clear_selection()
                    self.file_tree.selection_add(item)
                
                self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def on_file_double_click(self, event):
        """Handle double-click on file"""
        item = self.file_tree.identify_row(event.y)
        if not item:
            return
        
        values = self.file_tree.item(item)['values']
        if not values or len(values) < 1:
            return
        
        name = values[0]
        
        if name == '..':
            self.core.change_directory('..')
            self.refresh_files()
            return
        
        filepath = str(Path(self.core.current_dir) / name)
        
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File not found: {filepath}")
            return
        
        if os.path.isdir(filepath):
            self.core.change_directory(name)
            self.refresh_files()
        else:
            if filepath.endswith('.ezlock'):
                result = messagebox.askyesnocancel(
                    "Encrypted File",
                    "What would you like to do?\n\nYes - Edit file\nNo - Preview\nCancel - Cancel"
                )
                if result is True:
                    self.secure_edit_file(filepath)
                elif result is False:
                    password = self.shared_password_var.get() if self.shared_password_var.get() else None
                    if not password and not self.core.current_user:
                        password = simpledialog.askstring(
                            "Password Required",
                            "Enter password:",
                            show='*'
                        )
                        if password is None:
                            return
                    self.preview_file(filepath, password)
            else:
                self.preview_normal_file(filepath)
    
    def update_action_buttons(self):
        """Show/hide action buttons based on selection"""
        for widget in self.action_buttons_frame.winfo_children():
            widget.destroy()
        
        selected = self.get_selected_files()
        
        if selected:
            has_encrypted = any(f.endswith('.ezlock') for f in selected)
            has_normal = any(not f.endswith('.ezlock') and os.path.isfile(f) for f in selected)
            has_streaming = any(os.path.splitext(f)[1].lower() in self.core.streaming_formats for f in selected)
            
            row1 = tk.Frame(self.action_buttons_frame, bg='#ffffff')
            row1.pack(fill=tk.X, pady=2)
            
            row2 = tk.Frame(self.action_buttons_frame, bg='#ffffff')
            row2.pack(fill=tk.X, pady=2)
            
            row3 = tk.Frame(self.action_buttons_frame, bg='#ffffff')
            row3.pack(fill=tk.X, pady=2)
            
            if has_normal and not has_streaming:
                tk.Button(
                    row1,
                    text="Encrypt (Account)",
                    command=self.encrypt_selected,
                    bg='#4CAF50',
                    fg='white',
                    bd=0,
                    padx=10,
                    pady=5,
                    cursor='hand2',
                    font=('Arial', 9, 'bold')
                ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
                
                tk.Button(
                    row1,
                    text="Encrypt (Password)",
                    command=self.show_shared_encryption_dialog,
                    bg='#9C27B0',
                    fg='white',
                    bd=0,
                    padx=10,
                    pady=5,
                    cursor='hand2',
                    font=('Arial', 9, 'bold')
                ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            if has_streaming:
                tk.Label(
                    row1,
                    text="⚠️ Streaming formats cannot be encrypted",
                    fg='#F44336',
                    bg='#ffffff',
                    font=('Arial', 9, 'bold')
                ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            if has_encrypted:
                tk.Button(
                    row1,
                    text="Decrypt (Account)",
                    command=self.decrypt_selected,
                    bg='#2196F3',
                    fg='white',
                    bd=0,
                    padx=10,
                    pady=5,
                    cursor='hand2',
                    font=('Arial', 9, 'bold')
                ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
                
                tk.Button(
                    row1,
                    text="Decrypt (Password)",
                    command=self.show_shared_decryption_dialog,
                    bg='#673AB7',
                    fg='white',
                    bd=0,
                    padx=10,
                    pady=5,
                    cursor='hand2',
                    font=('Arial', 9, 'bold')
                ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            tk.Button(
                row2,
                text="Secure Edit",
                command=self.secure_edit_selected if has_encrypted else lambda: None,
                bg='#9C27B0',
                fg='white',
                bd=0,
                padx=10,
                pady=5,
                cursor='hand2',
                font=('Arial', 9, 'bold'),
                state=tk.NORMAL if has_encrypted else tk.DISABLED
            ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            tk.Button(
                row2,
                text="Preview",
                command=self.preview_selected,
                bg='#FF9800',
                fg='white',
                bd=0,
                padx=10,
                pady=5,
                cursor='hand2',
                font=('Arial', 9, 'bold')
            ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            tk.Button(
                row2,
                text="Delete",
                command=self.delete_selected,
                bg='#F44336',
                fg='white',
                bd=0,
                padx=10,
                pady=5,
                cursor='hand2',
                font=('Arial', 9, 'bold')
            ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            if len(selected) == 1 and os.path.isdir(selected[0]):
                folder = selected[0]
                if folder in self.core.secure_folders:
                    btn_text = "Remove Folder Security"
                    btn_color = '#FF9800'
                else:
                    btn_text = "Secure This Folder"
                    btn_color = '#9C27B0'
                
                tk.Button(
                    row3,
                    text=btn_text,
                    command=lambda f=folder: self.toggle_folder_security(f),
                    bg=btn_color,
                    fg='white',
                    bd=0,
                    padx=10,
                    pady=5,
                    cursor='hand2',
                    font=('Arial', 9, 'bold')
                ).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
    
    def toggle_folder_security(self, folder):
        """Toggle folder security"""
        if folder in self.core.secure_folders:
            success, message = self.core.stop_folder_watching(folder)
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
        else:
            success, message = self.core.start_folder_watching(
                folder,
                include_subfolders=True,
                password=None
            )
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
        
        self.refresh_files()
    
    def encrypt_selected(self):
        """Encrypt selected file(s)"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        streaming = [f for f in files if os.path.splitext(f)[1].lower() in self.core.streaming_formats]
        if streaming:
            messagebox.showerror("Error", "Streaming formats cannot be encrypted!")
            return
        
        if len(files) > 1:
            self.batch_encrypt()
        elif files:
            filepath = files[0]
            if not os.path.isdir(filepath) and not filepath.endswith('.ezlock'):
                self.encrypt_file(filepath)
    
    def decrypt_selected(self):
        """Decrypt selected file(s)"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        if len(files) > 1:
            self.batch_decrypt()
        elif files:
            filepath = files[0]
            if filepath.endswith('.ezlock'):
                self.decrypt_file(filepath)
    
    def preview_selected(self):
        """Preview selected file"""
        files = self.get_selected_files()
        if not files:
            return
        
        filepath = files[0]
        
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File not found: {filepath}")
            return
        
        if filepath.endswith('.ezlock'):
            password = self.shared_password_var.get() if self.shared_password_var.get() else None
            if not password and not self.core.current_user:
                password = simpledialog.askstring(
                    "Password Required",
                    "Enter password:",
                    show='*'
                )
                if password is None:
                    return
            self.preview_file(filepath, password)
        else:
            self.preview_normal_file(filepath)
    
    def delete_selected(self):
        """Delete selected files"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        if self.confirm_before_delete_var.get():
            result = messagebox.askyesno(
                "Delete Files",
                f"Delete {len(files)} file(s)?"
            )
            if not result:
                return
        
        success_count = 0
        for filepath in files:
            try:
                os.remove(filepath)
                success_count += 1
            except:
                pass
        
        messagebox.showinfo("Success", f"Deleted {success_count} file(s)")
        self.refresh_files()
        self.clear_preview()
        self.clear_selection()
    
    def show_shared_encryption_dialog(self):
        """Show dialog for password encryption"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "Please select files to encrypt")
            return
        
        streaming = [f for f in files if os.path.splitext(f)[1].lower() in self.core.streaming_formats]
        if streaming:
            messagebox.showerror("Error", "Streaming formats cannot be encrypted!")
            return
        
        password = self.shared_password_var.get()
        
        if not password:
            messagebox.showinfo("Info", "Please enter a password first")
            self.shared_password_entry.focus()
            return
        
        random_name = self.random_filename_var.get()
        
        if len(files) > 1:
            progress = tk.Toplevel(self.root)
            progress.title("Batch Encryption")
            progress.geometry("400x150")
            progress.transient(self.root)
            
            tk.Label(progress, text="Encrypting with password...", font=('Arial', 11)).pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress, length=300, mode='determinate')
            progress_bar.pack(pady=10)
            
            status_label = tk.Label(progress, text="")
            status_label.pack()
            
            progress_bar['maximum'] = len(files)
            
            success_count = 0
            for i, filepath in enumerate(files):
                if not filepath.endswith('.ezlock') and os.path.isfile(filepath):
                    status_label.config(text=f"Encrypting: {os.path.basename(filepath)}")
                    progress_bar['value'] = i + 1
                    progress.update()
                    
                    success, message = self.core.encrypt_file(
                        filepath,
                        password=password,
                        random_name=random_name
                    )
                    if success:
                        success_count += 1
            
            progress.destroy()
            
            messagebox.showinfo(
                "Complete",
                f"[+] Encrypted {success_count} of {len(files)} files (saved as .ezlock)"
            )
        else:
            success, message = self.core.encrypt_file(
                files[0],
                password=password,
                random_name=random_name
            )
            
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
        
        self.refresh_files()
    
    def show_shared_decryption_dialog(self):
        """Show dialog for password decryption"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "Please select encrypted files to decrypt")
            return
        
        to_decrypt = [f for f in files if f.endswith('.ezlock')]
        
        if not to_decrypt:
            messagebox.showinfo("Info", "No encrypted files selected (expected .ezlock)")
            return
        
        password = self.shared_password_var.get()
        
        if not password:
            messagebox.showinfo("Info", "Please enter a password first")
            self.shared_password_entry.focus()
            return
        
        if len(to_decrypt) > 1:
            progress = tk.Toplevel(self.root)
            progress.title("Batch Decryption")
            progress.geometry("400x150")
            progress.transient(self.root)
            
            tk.Label(progress, text="Decrypting with password...", font=('Arial', 11)).pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress, length=300, mode='determinate')
            progress_bar.pack(pady=10)
            
            status_label = tk.Label(progress, text="")
            status_label.pack()
            
            progress_bar['maximum'] = len(to_decrypt)
            
            success_count = 0
            for i, filepath in enumerate(to_decrypt):
                status_label.config(text=f"Decrypting: {os.path.basename(filepath)}")
                progress_bar['value'] = i + 1
                progress.update()
                
                success, message, data = self.core.decrypt_file(
                    filepath,
                    password=password
                )
                if success:
                    success_count += 1
            
            progress.destroy()
            
            messagebox.showinfo(
                "Complete",
                f"[+] Decrypted {success_count} of {len(to_decrypt)} files"
            )
        else:
            success, message, data = self.core.decrypt_file(
                to_decrypt[0],
                password=password
            )
            
            if success:
                filename, metadata = data
                messagebox.showinfo("Success", message)
                if filename and os.path.exists(filename):
                    self.preview_normal_file(filename)
            else:
                messagebox.showerror("Error", message)
        
        self.refresh_files()
    
    def encrypt_file(self, filepath, password=None):
        """Encrypt a file"""
        random_name = self.random_filename_var.get()
        
        success, message = self.core.encrypt_file(
            filepath,
            password=password,
            random_name=random_name
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.status_bar.config(text=message)
            self.refresh_files()
        else:
            messagebox.showerror("Error", message)
    
    def decrypt_file(self, filepath, password=None):
        """Decrypt a file"""
        success, message, data = self.core.decrypt_file(
            filepath,
            password=password
        )
        
        if success:
            filename, metadata = data
            messagebox.showinfo("Success", message)
            self.status_bar.config(text=message)
            self.refresh_files()
            
            if filename and os.path.exists(filename):
                self.preview_normal_file(filename)
        else:
            messagebox.showerror("Error", message)
    
    def preview_normal_file(self, filepath):
        """Preview non-encrypted file"""
        try:
            self.stop_video()
            self.stop_audio()
            self.clear_preview()
            
            self.current_preview_file = filepath
            self.current_preview_is_encrypted = False
            self.current_preview_data = None
            self.current_preview_metadata = None
            
            size = os.path.getsize(filepath)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            self.preview_info_label.config(
                text=f"Size: {self.core.format_size(size)} | Modified: {mtime.strftime('%Y-%m-%d %H:%M')}"
            )
            
            with open(filepath, 'rb') as f:
                header = f.read(12)
            
            ext = os.path.splitext(filepath)[1].lower()
            
            modes = ["auto", "text", "hex"]
            file_type = "unknown"
            
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', '.webp'] or \
               header.startswith(b'\x89PNG') or header.startswith(b'\xff\xd8') or header.startswith(b'GIF'):
                modes.insert(1, "original")
                file_type = "image"
            elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm'] or \
                 header.startswith(b'\x00\x00\x00\x18ftyp') or header.startswith(b'\x00\x00\x00\x1cftyp'):
                modes.insert(1, "original")
                file_type = "video"
            elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'] or \
                 header.startswith(b'ID3') or header.startswith(b'OggS'):
                modes.insert(1, "original")
                file_type = "audio"
            elif ext == '.pdf' or header.startswith(b'%PDF'):
                modes.insert(1, "original")
                file_type = "pdf"
            else:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        f.read(100)
                    file_type = "text"
                except:
                    file_type = "binary"
            
            self.mode_combo['values'] = modes
            if self.preview_mode.get() not in modes:
                self.preview_mode.set("auto")
            
            self.show_preview_by_mode(filepath, file_type, header)
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot preview: {str(e)}")
    
    def show_preview_by_mode(self, filepath, file_type, header=None):
        """Show preview based on selected mode"""
        mode = self.preview_mode.get()
        
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_text.pack_forget()
        self.video_controls.pack_forget()
        self.audio_controls.pack_forget()
        self.pdf_controls.pack_forget()
        
        if mode == "original" and file_type in ["image", "video", "audio", "pdf"]:
            if file_type == "image" and PIL_AVAILABLE:
                self.show_image_preview(filepath)
            elif file_type == "video" and CV2_AVAILABLE:
                self.show_video_preview(filepath)
            elif file_type == "audio":
                self.show_audio_preview(filepath)
            elif file_type == "pdf" and PYMUPDF_AVAILABLE:
                self.show_pdf_preview(filepath)
            else:
                self.show_text_preview(filepath)
        elif mode == "text" or (mode == "auto" and file_type == "text"):
            self.preview_canvas.pack_forget()
            self.preview_text.pack(fill=tk.BOTH, expand=True)
            self.show_text_preview(filepath)
        elif mode == "hex" or (mode == "auto" and file_type == "binary"):
            self.preview_canvas.pack_forget()
            self.preview_text.pack(fill=tk.BOTH, expand=True)
            self.show_hex_preview(filepath)
        elif mode == "auto" and file_type in ["image", "video", "audio", "pdf"]:
            if file_type == "image" and PIL_AVAILABLE:
                self.show_image_preview(filepath)
            elif file_type == "video" and CV2_AVAILABLE:
                self.show_video_preview(filepath)
            elif file_type == "audio":
                self.show_audio_preview(filepath)
            elif file_type == "pdf" and PYMUPDF_AVAILABLE:
                self.show_pdf_preview(filepath)
            else:
                self.show_text_preview(filepath)
        else:
            self.preview_canvas.delete('all')
            msg = f"Cannot preview this file type.\nTry text or hex mode."
            self.preview_canvas.create_text(
                self.preview_canvas.winfo_width() // 2,
                self.preview_canvas.winfo_height() // 2,
                text=msg,
                fill='#666666',
                font=('Arial', 12),
                justify=tk.CENTER
            )
    
    def show_text_preview(self, filepath):
        """Show text preview"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read(50000)
            
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', text)
            if os.path.getsize(filepath) > 50000:
                self.preview_text.insert(tk.END, "\n\n... (file truncated)")
            
            self.status_bar.config(text=f"Text preview: {os.path.basename(filepath)}")
            
        except Exception as e:
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', f"Error: {str(e)}")
    
    def show_hex_preview(self, filepath):
        """Show hexadecimal preview"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read(2048)
            
            hex_lines = []
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                hex_str = ' '.join(f'{b:02x}' for b in chunk)
                ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                hex_lines.append(f'{i:08x}  {hex_str:<48}  {ascii_str}')
            
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', '\n'.join(hex_lines))
            if os.path.getsize(filepath) > 2048:
                self.preview_text.insert(tk.END, f"\n\n... (showing first 2KB)")
            
            self.status_bar.config(text=f"Hex preview: {os.path.basename(filepath)}")
            
        except Exception as e:
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', f"Error: {str(e)}")
    
    def show_image_preview(self, filepath):
        """Show image preview"""
        if not PIL_AVAILABLE:
            self.show_text_preview(filepath)
            return
        
        try:
            image = Image.open(filepath)
            
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width < 10:
                canvas_width = 500
                canvas_height = 400
            
            ratio = min(canvas_width / image.width, canvas_height / image.height) * 0.9
            if ratio > 1:
                ratio = 1
            
            new_size = (int(image.width * ratio), int(image.height * ratio))
            
            if ratio < 1:
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            self.preview_canvas.delete('all')
            self.preview_canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=photo,
                anchor=tk.CENTER
            )
            
            self.preview_canvas.image = photo
            self.status_bar.config(text=f"Image: {os.path.basename(filepath)}")
            
        except Exception as e:
            self.show_text_preview(filepath)
    
    def show_video_preview(self, filepath):
        """Show video preview with smooth playback using optimized player"""
        if not CV2_AVAILABLE:
            self.show_text_preview(filepath)
            return
        
        try:
            # Stop any existing playback
            self.stop_video()
            
            # Create new optimized video player
            self.video_player = OptimizedVideoPlayer(self.preview_canvas, self.video_controls_callback)
            self.video_player.set_root(self.root)
            
            # Load video into player
            if self.video_player.load_video(filepath):
                # Get video info
                info = {
                    'duration': self.video_player.duration,
                    'fps': self.video_player.fps,
                    'frames': self.video_player.total_frames
                }
                
                self.preview_info_label.config(
                    text=f"Duration: {info['duration']:.1f}s | FPS: {info['fps']:.1f} | Frames: {info['frames']}"
                )
                
                # Enable controls
                self.play_btn.config(state=tk.NORMAL)
                self.pause_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.NORMAL)
                self.fullscreen_btn.config(state=tk.NORMAL)
                
                # Set initial FPS
                self.fps_var.set(str(min(60, max(15, int(self.video_player.fps)))))
                self.on_fps_change()
                
                # Show controls
                self.video_controls.pack(fill=tk.X, pady=2)
                self.audio_controls.pack_forget()
                self.pdf_controls.pack_forget()
                
                # Reset timeline
                self.video_timeline.set(0)
                self.video_time_label.config(text="00:00 / 00:00")
                
                # Auto-play the video
                self.play_video()
            else:
                self.show_text_preview(filepath)
            
        except Exception as e:
            print(f"Video preview error: {e}")
            self.show_text_preview(filepath)
    
    def video_seek(self, value):
        """Seek video to position"""
        if self.video_player:
            self.video_player.seek(float(value))
    
    def play_video(self):
        """Play video"""
        if self.video_player:
            self.video_player.play()
            self.play_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
    
    def pause_video(self):
        """Pause video"""
        if self.video_player:
            self.video_player.pause()
            if self.video_player.paused:
                self.pause_btn.config(state=tk.NORMAL)
                self.play_btn.config(state=tk.NORMAL)
            else:
                self.play_btn.config(state=tk.DISABLED)
                self.pause_btn.config(state=tk.NORMAL)
    
    def stop_video(self):
        """Stop video"""
        if self.video_player:
            self.video_player.stop()
        
        if hasattr(self, 'play_btn') and self.play_btn:
            self.play_btn.config(state=tk.DISABLED)
        if hasattr(self, 'pause_btn') and self.pause_btn:
            self.pause_btn.config(state=tk.DISABLED)
        if hasattr(self, 'stop_btn') and self.stop_btn:
            self.stop_btn.config(state=tk.DISABLED)
        if hasattr(self, 'fullscreen_btn') and self.fullscreen_btn:
            self.fullscreen_btn.config(state=tk.DISABLED)
        if hasattr(self, 'video_timeline') and self.video_timeline:
            self.video_timeline.set(0)
        if hasattr(self, 'video_time_label') and self.video_time_label:
            self.video_time_label.config(text="00:00 / 00:00")
        if hasattr(self, 'video_controls'):
            self.video_controls.pack_forget()
    
    def set_volume(self, value):
        """Set video volume"""
        if self.video_player:
            self.video_player.set_volume(float(value))
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode for video"""
        if self.video_player:
            self.video_player.toggle_fullscreen(self.root, self.preview_canvas)
    
    def show_audio_preview(self, filepath):
        """Show audio preview with waveform and frequency spectrum"""
        if not PYGAME_AVAILABLE:
            messagebox.showinfo("Info", "Pygame not installed. Install with: pip install pygame")
            self.show_text_preview(filepath)
            return
        
        self.stop_audio()
        
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            
            self.audio_file = filepath
            
            # Get audio info
            audio_info = AudioAnalyzer.get_audio_info(filepath)
            self.audio_duration = audio_info['duration']
            
            # Generate waveform
            self.audio_waveform = AudioAnalyzer.generate_waveform(filepath, points=500)
            
            # Generate spectrum
            if CV2_AVAILABLE and PYDUB_AVAILABLE:
                try:
                    # Load audio for spectrum analysis
                    audio = AudioSegment.from_file(filepath)
                    if audio.channels > 1:
                        audio = audio.set_channels(1)
                    samples = np.array(audio.get_array_of_samples())
                    self.audio_data_buffer = samples
                    # Initial spectrum
                    spectrum_data = AudioAnalyzer.compute_spectrum(samples[:2048], audio.frame_rate)
                    self.audio_spectrum = spectrum_data.get('full', [])
                except:
                    self.audio_spectrum = []
            else:
                self.audio_spectrum = []
            
            # Set up timeline
            self.audio_timeline.config(to=100)
            self.audio_timeline.set(0)
            
            minutes = int(self.audio_duration // 60)
            seconds = int(self.audio_duration % 60)
            self.preview_info_label.config(
                text=f"Audio: {os.path.basename(filepath)} | Duration: {minutes:02d}:{seconds:02d}"
            )
            
            # Enable controls
            self.audio_play_btn.config(state=tk.NORMAL)
            self.audio_pause_btn.config(state=tk.NORMAL)
            self.audio_stop_btn.config(state=tk.NORMAL)
            
            # Show controls
            self.audio_controls.pack(fill=tk.X, pady=2)
            self.video_controls.pack_forget()
            self.pdf_controls.pack_forget()
            
            self.audio_time_label.config(text=f"00:00 / {minutes:02d}:{seconds:02d}")
            
            # Draw waveform and spectrum
            self.root.after(100, self.refresh_audio_visualization)
            
        except Exception as e:
            print(f"Audio preview error: {e}")
            messagebox.showerror("Audio Error", f"Cannot play audio: {str(e)}")
            self.show_text_preview(filepath)
    
    def refresh_audio_visualization(self):
        """Refresh audio waveform and spectrum displays"""
        self.draw_audio_waveform()
        self.draw_audio_spectrum()
    
    def draw_audio_waveform(self):
        """Draw audio waveform on canvas"""
        if not self.audio_waveform or not self.audio_canvas:
            return
        
        self.audio_canvas.delete('waveform')
        width = self.audio_canvas.winfo_width()
        height = self.waveform_height
        
        if width < 10:
            return
        
        points = len(self.audio_waveform)
        x_step = width / points
        
        # Draw waveform line
        coords = []
        for i, amp in enumerate(self.audio_waveform):
            x = i * x_step
            y = height - (amp * height * 0.8) - 5
            coords.extend([x, y])
        
        if len(coords) >= 4:
            self.audio_canvas.create_line(coords, fill='#00ff00', width=2, tags='waveform')
        
        # Draw playhead position line
        if self.audio_duration > 0 and self.audio_position > 0:
            playhead_x = (self.audio_position / self.audio_duration) * width
            self.audio_canvas.create_line(
                playhead_x, 5, playhead_x, height - 5,
                fill='#ff0000', width=2, tags='playhead'
            )
    
    def draw_audio_spectrum(self):
        """Draw audio frequency spectrum on canvas"""
        if not self.audio_spectrum or not self.audio_spectrum_canvas:
            return
        
        self.audio_spectrum_canvas.delete('spectrum')
        width = self.audio_spectrum_canvas.winfo_width()
        height = self.spectrum_height
        
        if width < 10:
            return
        
        points = len(self.audio_spectrum)
        if points == 0:
            return
        
        bar_width = max(2, width // points)
        bar_spacing = 1
        
        # Draw frequency bars
        for i, amplitude in enumerate(self.audio_spectrum[:points]):
            x = i * (bar_width + bar_spacing)
            bar_height = amplitude * height
            if bar_height > 2:
                # Color based on frequency range
                if i < points // 4:  # Bass
                    color = '#ff4444'
                elif i < points // 2:  # Mid
                    color = '#44ff44'
                else:  # Treble
                    color = '#4444ff'
                
                self.audio_spectrum_canvas.create_rectangle(
                    x, height - bar_height, x + bar_width, height,
                    fill=color, outline='', tags='spectrum'
                )
        
        # Draw bass/mid/treble labels
        self.audio_spectrum_canvas.delete('labels')
        if hasattr(self, 'audio_analyzer') and self.audio_data_buffer is not None:
            try:
                # Get current spectrum data if playing
                audio = AudioSegment.from_file(self.audio_file)
                if audio.channels > 1:
                    audio = audio.set_channels(1)
                # Get a segment around current position
                pos_ms = int(self.audio_position * 1000)
                segment = audio[pos_ms:pos_ms+2048]
                if len(segment) > 0:
                    samples = np.array(segment.get_array_of_samples())
                    spectrum = AudioAnalyzer.compute_spectrum(samples, audio.frame_rate)
                    bass = spectrum.get('bass', 0)
                    mid = spectrum.get('mid', 0)
                    treble = spectrum.get('treble', 0)
                    
                    # Draw indicators
                    self.audio_spectrum_canvas.create_text(
                        10, 10, text=f"Bass: {bass:.2f}", fill='#ff4444', anchor=tk.NW, tags='labels'
                    )
                    self.audio_spectrum_canvas.create_text(
                        10, 25, text=f"Mid: {mid:.2f}", fill='#44ff44', anchor=tk.NW, tags='labels'
                    )
                    self.audio_spectrum_canvas.create_text(
                        10, 40, text=f"Treble: {treble:.2f}", fill='#4444ff', anchor=tk.NW, tags='labels'
                    )
            except:
                pass
    
    def play_audio(self):
        """Play audio file with proper position tracking"""
        if not hasattr(self, 'audio_file') or not self.audio_file:
            return
        
        try:
            if PYGAME_AVAILABLE:
                if self.audio_paused:
                    pygame.mixer.music.unpause()
                    self.audio_paused = False
                    self.audio_playing = True
                    self.audio_pause_btn.config(text="⏸", bg='#FF9800')
                    self.audio_play_btn.config(state=tk.DISABLED)
                    self.update_audio()
                else:
                    # Start from beginning or current position
                    if self.audio_position > 0 and self.audio_position < self.audio_duration:
                        pygame.mixer.music.load(self.audio_file)
                        pygame.mixer.music.play(start=self.audio_position)
                    else:
                        pygame.mixer.music.load(self.audio_file)
                        pygame.mixer.music.play()
                        self.audio_position = 0
                    
                    pygame.mixer.music.set_volume(self.audio_volume_var.get() / 100.0)
                    self.audio_playing = True
                    self.audio_paused = False
                    self.audio_play_btn.config(state=tk.DISABLED)
                    self.audio_pause_btn.config(state=tk.NORMAL)
                    self.audio_stop_btn.config(state=tk.NORMAL)
                    self.update_audio()
        except Exception as e:
            messagebox.showerror("Audio Error", f"Cannot play: {str(e)}")
    
    def pause_audio(self):
        """Pause audio playback"""
        if not self.audio_playing:
            return
        
        if PYGAME_AVAILABLE:
            pygame.mixer.music.pause()
            self.audio_paused = True
            self.audio_pause_btn.config(text="▶", bg='#4CAF50')
            self.audio_play_btn.config(state=tk.NORMAL)
    
    def stop_audio(self):
        """Stop audio playback"""
        if PYGAME_AVAILABLE:
            pygame.mixer.music.stop()
        
        self.audio_playing = False
        self.audio_paused = False
        self.audio_position = 0
        
        if self.audio_update_job:
            self.root.after_cancel(self.audio_update_job)
            self.audio_update_job = None
        
        if hasattr(self, 'audio_play_btn') and self.audio_play_btn:
            self.audio_play_btn.config(state=tk.NORMAL)
        if hasattr(self, 'audio_pause_btn') and self.audio_pause_btn:
            self.audio_pause_btn.config(state=tk.DISABLED, text="⏸", bg='#FF9800')
        if hasattr(self, 'audio_stop_btn') and self.audio_stop_btn:
            self.audio_stop_btn.config(state=tk.DISABLED)
        if hasattr(self, 'audio_timeline') and self.audio_timeline:
            self.audio_timeline.set(0)
        if hasattr(self, 'audio_time_label') and self.audio_time_label:
            self.audio_time_label.config(text="00:00 / 00:00")
        
        # Clear waveform playhead
        if self.audio_canvas:
            self.audio_canvas.delete('playhead')
            self.draw_audio_waveform()
        
        if self.audio_spectrum_canvas:
            self.audio_spectrum_canvas.delete('labels')
    
    def audio_seek(self, value):
        """Seek audio to position"""
        if not hasattr(self, 'audio_file') or not self.audio_file:
            return
        
        position = (float(value) / 100) * self.audio_duration
        self.audio_position = position
        
        if PYGAME_AVAILABLE and self.audio_playing:
            # Restart playback at new position
            was_playing = self.audio_playing and not self.audio_paused
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.audio_file)
            if was_playing:
                pygame.mixer.music.play(start=position)
                pygame.mixer.music.set_volume(self.audio_volume_var.get() / 100.0)
        
        minutes = int(position // 60)
        seconds = int(position % 60)
        total_minutes = int(self.audio_duration // 60)
        total_seconds = int(self.audio_duration % 60)
        self.audio_time_label.config(
            text=f"{minutes:02d}:{seconds:02d} / {total_minutes:02d}:{total_seconds:02d}"
        )
        
        # Update waveform playhead
        if self.audio_canvas:
            self.audio_canvas.delete('playhead')
            self.draw_audio_waveform()
        
        # Update spectrum
        if self.audio_spectrum_canvas and self.audio_data_buffer is not None:
            self.draw_audio_spectrum()
    
    def set_audio_volume(self, value):
        """Set audio volume"""
        if PYGAME_AVAILABLE:
            pygame.mixer.music.set_volume(float(value) / 100.0)
    
    def update_audio(self):
        """Update audio position and timeline"""
        if not self.audio_playing or self.audio_paused:
            return
        
        if PYGAME_AVAILABLE and pygame.mixer.music.get_busy():
            # Get current position (approximate)
            # Since pygame doesn't provide exact position, we increment
            self.audio_position += 0.1
        else:
            if self.audio_playing:
                self.stop_audio()
            return
        
        if self.audio_position >= self.audio_duration:
            self.stop_audio()
            return
        
        percentage = (self.audio_position / self.audio_duration) * 100
        self.audio_timeline.set(percentage)
        
        minutes = int(self.audio_position // 60)
        seconds = int(self.audio_position % 60)
        total_minutes = int(self.audio_duration // 60)
        total_seconds = int(self.audio_duration % 60)
        self.audio_time_label.config(
            text=f"{minutes:02d}:{seconds:02d} / {total_minutes:02d}:{total_seconds:02d}"
        )
        
        # Update waveform playhead
        if self.audio_canvas:
            self.audio_canvas.delete('playhead')
            self.draw_audio_waveform()
        
        # Update spectrum in real-time
        if self.audio_spectrum_canvas and self.audio_data_buffer is not None and CV2_AVAILABLE and PYDUB_AVAILABLE:
            try:
                audio = AudioSegment.from_file(self.audio_file)
                if audio.channels > 1:
                    audio = audio.set_channels(1)
                pos_ms = int(self.audio_position * 1000)
                segment = audio[pos_ms:pos_ms+2048]
                if len(segment) > 0:
                    samples = np.array(segment.get_array_of_samples())
                    spectrum = AudioAnalyzer.compute_spectrum(samples, audio.frame_rate)
                    self.audio_spectrum = spectrum.get('full', [])
                    self.draw_audio_spectrum()
            except:
                pass
        
        self.audio_update_job = self.root.after(100, self.update_audio)
    
    def show_pdf_preview(self, filepath):
        """Show PDF preview"""
        if not PYMUPDF_AVAILABLE:
            self.show_text_preview(filepath)
            return
        
        try:
            self.pdf_document = fitz.open(filepath)
            self.pdf_total_pages = len(self.pdf_document)
            self.pdf_page = 0
            
            self.pdf_prev_btn.config(state=tk.NORMAL if self.pdf_total_pages > 1 else tk.DISABLED)
            self.pdf_next_btn.config(state=tk.NORMAL if self.pdf_total_pages > 1 else tk.DISABLED)
            self.pdf_controls.pack(fill=tk.X, pady=2)
            self.video_controls.pack_forget()
            self.audio_controls.pack_forget()
            
            self.show_pdf_page()
            self.status_bar.config(text=f"PDF: {os.path.basename(filepath)} | {self.pdf_total_pages} pages")
            
        except Exception as e:
            self.show_text_preview(filepath)
    
    def show_pdf_page(self):
        """Show current PDF page"""
        if not PYMUPDF_AVAILABLE or not self.pdf_document:
            return
        
        try:
            page = self.pdf_document[self.pdf_page]
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat)
            
            img_data = pix.tobytes("png")
            
            temp_file = self.core.temp_dir / f"pdf_page_{self.pdf_page}.png"
            with open(temp_file, 'wb') as f:
                f.write(img_data)
            
            self.core.add_temp_file(str(temp_file))
            self.preview_temp_files.append(str(temp_file))
            
            image = Image.open(temp_file)
            
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width < 10:
                canvas_width = 500
                canvas_height = 700
            
            ratio = min(canvas_width / image.width, canvas_height / image.height) * 0.9
            if ratio > 1:
                ratio = 1
                
            new_size = (int(image.width * ratio), int(image.height * ratio))
            
            if ratio < 1:
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            self.preview_canvas.delete('all')
            self.preview_canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=photo,
                anchor=tk.CENTER
            )
            
            self.preview_canvas.image = photo
            self.pdf_page_label.config(text=f"Page {self.pdf_page + 1}/{self.pdf_total_pages}")
            
        except Exception as e:
            pass
    
    def pdf_prev_page(self):
        """Go to previous PDF page"""
        if self.pdf_page > 0:
            self.pdf_page -= 1
            self.show_pdf_page()
    
    def pdf_next_page(self):
        """Go to next PDF page"""
        if self.pdf_page < self.pdf_total_pages - 1:
            self.pdf_page += 1
            self.show_pdf_page()
    
    def preview_file(self, filepath, password=None):
        """Preview encrypted file"""
        self.stop_video()
        self.stop_audio()
        
        success, message, preview_info = self.core.preview_file(filepath, password)
        
        if not success:
            messagebox.showerror("Error", message)
            return
        
        self.current_preview_file = filepath
        self.current_preview_is_encrypted = True
        self.current_preview_data = preview_info['data']
        self.current_preview_metadata = preview_info['metadata']
        
        metadata = preview_info['metadata']
        protected_status = "Password" if metadata.get('key_source') == 'password' else "Account"
        self.preview_info_label.config(
            text=f"Original: {metadata.get('original_name', 'unknown')} | Size: {self.core.format_size(len(preview_info['data']))} | {protected_status}"
        )
        
        ext = os.path.splitext(metadata.get('original_name', 'file.bin'))[1].lower()
        
        self.core.temp_dir.mkdir(parents=True, exist_ok=True)
        temp_file = self.core.temp_dir / f"preview_{secrets.token_hex(8)}{ext}"
        with open(temp_file, 'wb') as f:
            f.write(preview_info['data'])
        
        self.core.add_temp_file(str(temp_file))
        self.preview_temp_files.append(str(temp_file))
        self.current_preview_temp_file = str(temp_file)
        
        self.preview_normal_file(str(temp_file))
    
    def save_preview(self):
        """Save currently previewed file"""
        if not self.current_preview_file:
            return
        
        if self.current_preview_is_encrypted and self.current_preview_data:
            original_name = self.current_preview_metadata.get('original_name', 'decrypted_file') if self.current_preview_metadata else "decrypted_file"
            dest = filedialog.asksaveasfilename(
                initialdir=self.core.current_dir,
                initialfile=original_name,
                title="Save Decrypted File"
            )
            if dest:
                with open(dest, 'wb') as f:
                    f.write(self.current_preview_data)
                messagebox.showinfo("Success", f"File saved as: {dest}")
                self.refresh_files()
        else:
            dest = filedialog.asksaveasfilename(
                initialdir=self.core.current_dir,
                initialfile=os.path.basename(self.current_preview_file),
                title="Save File As"
            )
            if dest:
                shutil.copy2(self.current_preview_file, dest)
                messagebox.showinfo("Success", f"File saved as: {dest}")
    
    def refresh_preview(self):
        """Refresh preview for selected file"""
        if self.current_preview_file:
            if self.current_preview_is_encrypted:
                password = self.shared_password_var.get() if self.shared_password_var.get() else None
                if not password and not self.core.current_user:
                    password = simpledialog.askstring(
                        "Password Required",
                        "Enter password:",
                        show='*'
                    )
                    if password is None:
                        return
                self.preview_file(self.current_preview_file, password)
            else:
                self.preview_normal_file(self.current_preview_file)
    
    def clear_preview(self):
        """Clear preview area"""
        self.preview_canvas.delete('all')
        self.preview_text.delete('1.0', tk.END)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_text.pack_forget()
        self.video_controls.pack_forget()
        self.audio_controls.pack_forget()
        self.pdf_controls.pack_forget()
        self.preview_info_label.config(text="")
        
        self.stop_video()
        self.stop_audio()
        self.pdf_document = None
        
        self.preview_temp_files.clear()
        
        self.current_preview_file = None
        self.current_preview_data = None
        self.current_preview_metadata = None
        self.current_preview_temp_file = None
    
    def batch_encrypt(self):
        """Encrypt multiple selected files"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        to_encrypt = [f for f in files if os.path.isfile(f) and not f.endswith('.ezlock')]
        to_encrypt = [f for f in to_encrypt if os.path.splitext(f)[1].lower() not in self.core.streaming_formats]
        
        if not to_encrypt:
            messagebox.showinfo("Info", "No valid files to encrypt")
            return
        
        password = self.shared_password_var.get() if self.shared_password_var.get() else None
        random_name = self.random_filename_var.get()
        
        if not messagebox.askyesno("Batch Encrypt", f"Encrypt {len(to_encrypt)} file(s) as .ezlock?"):
            return
        
        progress = tk.Toplevel(self.root)
        progress.title("Batch Encryption")
        progress.geometry("400x150")
        progress.transient(self.root)
        
        tk.Label(progress, text="Encrypting files...", font=('Arial', 11)).pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress, length=300, mode='determinate')
        progress_bar.pack(pady=10)
        
        status_label = tk.Label(progress, text="")
        status_label.pack()
        
        progress_bar['maximum'] = len(to_encrypt)
        
        success_count = 0
        for i, filepath in enumerate(to_encrypt):
            status_label.config(text=f"Encrypting: {os.path.basename(filepath)}")
            progress_bar['value'] = i + 1
            progress.update()
            
            success, message = self.core.encrypt_file(
                filepath,
                password=password,
                random_name=random_name
            )
            if success:
                success_count += 1
        
        progress.destroy()
        
        messagebox.showinfo("Complete", f"[+] Encrypted {success_count} of {len(to_encrypt)} files (saved as .ezlock)")
        self.refresh_files()
        self.clear_selection()
    
    def batch_decrypt(self):
        """Decrypt multiple selected files"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        to_decrypt = [f for f in files if f.endswith('.ezlock')]
        
        if not to_decrypt:
            messagebox.showinfo("Info", "No encrypted files selected (expected .ezlock)")
            return
        
        password = self.shared_password_var.get() if self.shared_password_var.get() else None
        
        if not messagebox.askyesno("Batch Decrypt", f"Decrypt {len(to_decrypt)} file(s)?"):
            return
        
        progress = tk.Toplevel(self.root)
        progress.title("Batch Decryption")
        progress.geometry("400x150")
        progress.transient(self.root)
        
        tk.Label(progress, text="Decrypting files...", font=('Arial', 11)).pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress, length=300, mode='determinate')
        progress_bar.pack(pady=10)
        
        status_label = tk.Label(progress, text="")
        status_label.pack()
        
        progress_bar['maximum'] = len(to_decrypt)
        
        success_count = 0
        for i, filepath in enumerate(to_decrypt):
            status_label.config(text=f"Decrypting: {os.path.basename(filepath)}")
            progress_bar['value'] = i + 1
            progress.update()
            
            success, message, data = self.core.decrypt_file(
                filepath,
                password=password
            )
            if success:
                success_count += 1
        
        progress.destroy()
        
        messagebox.showinfo("Complete", f"[+] Decrypted {success_count} of {len(to_decrypt)} files")
        self.refresh_files()
        self.clear_selection()
    
    def encrypt_dialog(self):
        """Open file dialog for encryption"""
        filepaths = filedialog.askopenfilenames(
            initialdir=self.core.current_dir,
            title="Select files to encrypt"
        )
        if filepaths:
            streaming = [f for f in filepaths if os.path.splitext(f)[1].lower() in self.core.streaming_formats]
            if streaming:
                messagebox.showerror("Error", "Streaming formats cannot be encrypted!")
                return
            
            if len(filepaths) > 1:
                password = self.shared_password_var.get() if self.shared_password_var.get() else None
                random_name = self.random_filename_var.get()
                
                progress = tk.Toplevel(self.root)
                progress.title("Batch Encryption")
                progress.geometry("400x150")
                progress.transient(self.root)
                
                tk.Label(progress, text="Encrypting files...", font=('Arial', 11)).pack(pady=10)
                
                progress_bar = ttk.Progressbar(progress, length=300, mode='determinate')
                progress_bar.pack(pady=10)
                
                status_label = tk.Label(progress, text="")
                status_label.pack()
                
                progress_bar['maximum'] = len(filepaths)
                
                success_count = 0
                for i, filepath in enumerate(filepaths):
                    status_label.config(text=f"Encrypting: {os.path.basename(filepath)}")
                    progress_bar['value'] = i + 1
                    progress.update()
                    
                    success, message = self.core.encrypt_file(
                        filepath,
                        password=password,
                        random_name=random_name
                    )
                    if success:
                        success_count += 1
                
                progress.destroy()
                
                messagebox.showinfo("Complete", f"[+] Encrypted {success_count} of {len(filepaths)} files (saved as .ezlock)")
                self.refresh_files()
            else:
                self.encrypt_file(filepaths[0])
    
    def decrypt_dialog(self):
        """Open file dialog for decryption"""
        filepaths = filedialog.askopenfilenames(
            initialdir=self.core.current_dir,
            title="Select files to decrypt",
            filetypes=[("EzLock files", "*.ezlock"), ("All files", "*.*")]
        )
        if filepaths:
            if len(filepaths) > 1:
                password = self.shared_password_var.get() if self.shared_password_var.get() else None
                
                progress = tk.Toplevel(self.root)
                progress.title("Batch Decryption")
                progress.geometry("400x150")
                progress.transient(self.root)
                
                tk.Label(progress, text="Decrypting files...", font=('Arial', 11)).pack(pady=10)
                
                progress_bar = ttk.Progressbar(progress, length=300, mode='determinate')
                progress_bar.pack(pady=10)
                
                status_label = tk.Label(progress, text="")
                status_label.pack()
                
                progress_bar['maximum'] = len(filepaths)
                
                success_count = 0
                for i, filepath in enumerate(filepaths):
                    status_label.config(text=f"Decrypting: {os.path.basename(filepath)}")
                    progress_bar['value'] = i + 1
                    progress.update()
                    
                    success, message, data = self.core.decrypt_file(
                        filepath,
                        password=password
                    )
                    if success:
                        success_count += 1
                
                progress.destroy()
                
                messagebox.showinfo("Complete", f"[+] Decrypted {success_count} of {len(filepaths)} files")
                self.refresh_files()
            else:
                self.decrypt_file(filepaths[0])
    
    def preview_dialog(self):
        """Open file dialog for preview"""
        filepath = filedialog.askopenfilename(
            initialdir=self.core.current_dir,
            title="Select file to preview",
            filetypes=[("EzLock files", "*.ezlock"), ("All files", "*.*")]
        )
        if filepath:
            password = self.shared_password_var.get() if self.shared_password_var.get() else None
            if not password and not self.core.current_user:
                password = simpledialog.askstring(
                    "Password Required",
                    "Enter password:",
                    show='*'
                )
                if password is None:
                    return
            self.preview_file(filepath, password)
    
    def browse_directory(self):
        """Browse for directory"""
        directory = filedialog.askdirectory(initialdir=self.core.current_dir)
        if directory:
            self.core.current_dir = directory
            self.refresh_files()
    
    def go_back(self):
        """Go to parent directory"""
        self.core.change_directory('..')
        self.refresh_files()
    
    def secure_delete(self):
        """Securely delete selected files with overwrite"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        to_delete = [f for f in files if os.path.isfile(f)]
        
        if not to_delete:
            messagebox.showinfo("Info", "No files to delete")
            return
        
        if self.confirm_before_delete_var.get():
            result = messagebox.askyesno(
                "Secure Delete",
                f"Permanently delete {len(to_delete)} file(s) with 3-pass overwrite?\nThis cannot be undone!"
            )
            if not result:
                return
        
        success_count = 0
        for filepath in to_delete:
            try:
                with open(filepath, 'rb+') as f:
                    size = os.path.getsize(filepath)
                    for _ in range(3):
                        f.seek(0)
                        f.write(os.urandom(size))
                        f.flush()
                        os.fsync(f.fileno())
                os.remove(filepath)
                success_count += 1
            except:
                pass
        
        messagebox.showinfo("Success", f"Securely deleted {success_count} file(s)")
        self.refresh_files()
        self.clear_preview()
        self.clear_selection()
    
    def wipe_memory(self):
        """Wipe all sensitive data from memory"""
        success, message = self.core.wipe_memory()
        messagebox.showinfo("Memory Wipe", message)
    
    def open_terminal(self):
        """Open terminal in current directory"""
        try:
            if sys.platform == 'win32':
                subprocess.Popen(f'start cmd /k cd /d "{self.core.current_dir}"', shell=True)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', '-a', 'Terminal', self.core.current_dir])
            else:
                subprocess.Popen(['gnome-terminal', '--working-directory', self.core.current_dir])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open terminal: {e}")
    
    def show_properties(self):
        """Show file properties for selected file"""
        files = self.get_selected_files()
        if not files:
            messagebox.showinfo("Info", "No files selected")
            return
        
        filepath = files[0]
        
        if not os.path.exists(filepath):
            return
        
        stat = os.stat(filepath)
        
        properties = f"""File Properties
━━━━━━━━━━━━━━━━━━━━━━━━
Name: {os.path.basename(filepath)}
Path: {filepath}
Size: {self.core.format_size(stat.st_size)}
Created: {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}
Modified: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
Accessed: {datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')}

Type: {'Directory' if os.path.isdir(filepath) else 'File'}
"""
        
        if filepath.endswith('.ezlock'):
            properties += f"\n🔒 EzLock Encrypted File\n"
        
        ext = os.path.splitext(filepath)[1].lower()
        if ext in self.core.streaming_formats:
            properties += f"\n⚠️ Streaming Format - Cannot be encrypted\n"
        
        if os.path.isdir(filepath) and filepath in self.core.secure_folders:
            data = self.core.secure_folders[filepath]
            properties += f"\nSecure Folder: Yes\n"
            properties += f"   Include subfolders: {data.get('include_subfolders', True)}\n"
            properties += f"   Password protected: {'Yes' if data.get('password') else 'No'}\n"
        
        messagebox.showinfo("Properties", properties)
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("EzLock Settings")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General Settings
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        canvas = tk.Canvas(general_frame)
        scrollbar = ttk.Scrollbar(general_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Preview Settings
        preview_group = tk.LabelFrame(scrollable_frame, text="Preview Settings", padx=10, pady=10)
        preview_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Checkbutton(
            preview_group,
            text="Enable instant preview on selection",
            variable=self.instant_preview_var,
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=5)
        
        # File Operations
        file_group = tk.LabelFrame(scrollable_frame, text="File Operations", padx=10, pady=10)
        file_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Checkbutton(
            file_group,
            text="Confirm before delete",
            variable=self.confirm_before_delete_var,
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=5)
        
        tk.Checkbutton(
            file_group,
            text="Use random filename when encrypting (.ezlock)",
            variable=self.random_filename_var,
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=5)
        
        # File Browser
        browser_group = tk.LabelFrame(scrollable_frame, text="File Browser", padx=10, pady=10)
        browser_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Checkbutton(
            browser_group,
            text="Show hidden files",
            variable=self.show_hidden_files_var,
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=5)
        
        # Appearance
        appearance_group = tk.LabelFrame(scrollable_frame, text="Appearance", padx=10, pady=10)
        appearance_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(appearance_group, text="Theme:", font=('Arial', 10)).pack(anchor=tk.W)
        
        theme_combo = ttk.Combobox(
            appearance_group,
            textvariable=self.theme_var,
            values=["System", "Light", "Dark"],
            state="readonly",
            width=20
        )
        theme_combo.pack(anchor=tk.W, pady=5)
        
        # Security Settings
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Security")
        
        security_scroll = tk.Canvas(security_frame)
        security_scrollbar = ttk.Scrollbar(security_frame, orient="vertical", command=security_scroll.yview)
        security_scrollable = ttk.Frame(security_scroll)
        
        security_scrollable.bind(
            "<Configure>",
            lambda e: security_scroll.configure(scrollregion=security_scroll.bbox("all"))
        )
        
        security_scroll.create_window((0, 0), window=security_scrollable, anchor="nw")
        security_scroll.configure(yscrollcommand=security_scrollbar.set)
        
        security_scroll.pack(side="left", fill="both", expand=True)
        security_scrollbar.pack(side="right", fill="y")
        
        # Encryption Settings
        encrypt_group = tk.LabelFrame(security_scrollable, text="Encryption Settings", padx=10, pady=10)
        encrypt_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            encrypt_group,
            text=f"Current User: {self.core.current_user or 'Not logged in'}",
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W, pady=5)
        
        tk.Label(
            encrypt_group,
            text="Encryption: AES-256-GCM with Zero Headers",
            font=('Arial', 9),
            fg='#666666'
        ).pack(anchor=tk.W, pady=2)
        
        tk.Label(
            encrypt_group,
            text="File Extension: .ezlock",
            font=('Arial', 9, 'bold'),
            fg='#9C27B0'
        ).pack(anchor=tk.W, pady=2)
        
        # Streaming Formats
        stream_group = tk.LabelFrame(security_scrollable, text="Streaming Formats (Not Encryptable)", padx=10, pady=10)
        stream_group.pack(fill=tk.X, padx=10, pady=10)
        
        stream_text = ", ".join(self.core.streaming_formats)
        tk.Label(
            stream_group,
            text=stream_text,
            font=('Arial', 9),
            fg='#00BCD4',
            wraplength=400
        ).pack(anchor=tk.W, pady=5)
        
        # Secure Delete Settings
        delete_group = tk.LabelFrame(security_scrollable, text="Secure Delete", padx=10, pady=10)
        delete_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            delete_group,
            text="Overwrite passes: 3 (DoD 5220.22-M standard)",
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=5)
        
        # Folder Security Settings
        folder_group = tk.LabelFrame(security_scrollable, text="Folder Security", padx=10, pady=10)
        folder_group.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            folder_group,
            text="Secure folders are monitored for new/modified files",
            font=('Arial', 10),
            fg='#666666'
        ).pack(anchor=tk.W, pady=5)
        
        folders = self.core.get_secure_folders()
        if folders:
            tk.Label(
                folder_group,
                text=f"Active folders: {len(folders)}",
                font=('Arial', 10, 'bold')
            ).pack(anchor=tk.W, pady=5)
        
        # Info/About
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Info")
        
        info_text = """EzLock V1.0.0

Advanced File Encryption Suite with Zero Headers & Folder Security

Encryption: AES-256-GCM
Authentication: HMAC-SHA256
Key Derivation: Argon2id
File Extension: .ezlock

New Features:
- Zero headers - completely hidden file format
- Memory-only passwords
- Folder Security - auto-encrypt files in watched folders
- Secure Edit - double-click to edit encrypted files
- Streaming formats protection (never encrypted)
- Optimized Video timeline & fullscreen with smooth playback
- Audio waveform visualization & playback with frequency spectrum
- Subfolder support
- MIT License included
- Support developer with BTC

Security Features:
- No visible file structure
- Passwords never touch disk
- In-memory only preview
- Secure file deletion
- Hardware binding

Supported Previews:
- Images (PNG, JPEG, GIF, etc.)
- Videos (MP4, AVI, MOV, etc.) with smooth timeline, speed control, fullscreen
- Audio (MP3, WAV, FLAC, etc.) with waveform & frequency spectrum visualization
- PDF documents with page navigation
- Text files
- Binary/Hex view

© 2026 Ezlock V1 """
        
        tk.Label(
            info_frame,
            text=info_text,
            justify=tk.LEFT,
            font=('Arial', 10),
            padx=20,
            pady=20
        ).pack()
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Close",
            command=dialog.destroy,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            bd=0,
            padx=30,
            pady=8,
            cursor='hand2'
        ).pack()
    
    def show_commands(self):
        """Show available commands"""
        commands = """EzLock Commands

CLI Commands:
  help              - Show this help
  gui               - Launch GUI mode
  register          - Create new account
  login             - Login to account
  logout            - Logout current user
  whoami            - Show current user
  users             - List all users
  license           - Show MIT license
  support           - Show support info (BTC address)
  guide             - Show user guide
  
  ls                - List files
  cd <folder>       - Change directory
  pwd               - Show current directory
  cat <file>        - View text file
  rm <file>         - Delete file
  mv <src> <dst>    - Move/rename file
  cp <src> <dst>    - Copy file
  mkdir <name>      - Create directory
  
  enc <file>        - Encrypt file (account) → .ezlock
  enc -p <file>     - Encrypt with password → .ezlock
  enc -r <file>     - Encrypt with random name → .ezlock
  dec <file>        - Decrypt file (account) from .ezlock
  dec -p <file>     - Decrypt with password from .ezlock
  preview <file>    - Preview encrypted file
  edit <file>       - Secure edit encrypted file
  
  secure <folder>   - Secure a folder
  unsecure <folder> - Remove folder security
  folders           - List secure folders
  
  clear             - Clear screen
  history           - Show command history
  memwipe           - Wipe memory
  exit              - Exit

GUI Keyboard Shortcuts:
  Ctrl+A            - Select all
  Ctrl+Shift+A      - Clear selection
  Ctrl+E            - Encrypt (Account) → .ezlock
  Ctrl+Shift+E      - Encrypt (Password) / Secure Edit
  Ctrl+D            - Decrypt (Account) from .ezlock
  Ctrl+Shift+D      - Decrypt (Password) from .ezlock
  Ctrl+Shift+F      - Secure current folder
  Ctrl+P            - Preview
  F5                - Refresh
  Delete            - Delete"""
        
        messagebox.showinfo("EzLock Commands", commands)
    
    def show_about(self):
        """Show about dialog"""
        about = """EzLock V1.0.0
Advanced File Encryption Suite with Zero Headers & Folder Security

File Extension: .ezlock

New Features:
- Zero headers - completely hidden file format
- Memory-only passwords (auto-wiped on exit)
- Folder Security - auto-encrypt files in watched folders
- Secure Edit - edit encrypted files seamlessly
- Streaming formats protection (never encrypted)
- Optimized Video timeline & fullscreen with smooth playback
- Audio waveform visualization & playback
- Subfolder support
- MIT License
- Bitcoin donation support

Security Features:
- AES-256-GCM encryption
- HMAC-SHA256 integrity
- No passwords stored on disk
- Secure in-memory preview only
- Auto-encryption for secure folders

Supported Previews:
- Images (PNG, JPEG, GIF, BMP, WebP)
- Videos (MP4, AVI, MOV, MKV, WebM) with smooth timeline
- Audio (MP3, WAV, FLAC, AAC, OGG) with waveform & playback
- PDF documents with page navigation
- Text files
- Binary hex view

© 2026 Ezlock V1 """
        
        messagebox.showinfo("About EzLock", about)
    
    def logout(self):
        """Logout current user"""
        self.stop_video()
        self.stop_audio()
        self.core.logout()
        self.clear_preview()
        self.create_login_screen()
    
    def clear_screen(self):
        """Clear all widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        """Run the GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()


class EzLockCLI:
    """CLI Interface with built-in commands"""
    
    def __init__(self, core):
        self.core = core
        self.running = True
        self.history = []
    
    def print_help(self):
        """Print help message"""
        help_text = """
EZLOCK V1.0.0 - COMMANDS
═══════════════════════════════════════════════════
ACCOUNT COMMANDS:
  register                      - Create new account
  login                         - Login to account
  logout                        - Logout current user
  whoami                        - Show current user
  users                         - List all users

INFORMATION COMMANDS (NEW):
  license                       - Show MIT license
  support                       - Show support info (BTC address)
  guide                         - Show user guide

NAVIGATION COMMANDS:
  ls                            - List files
  cd [folder]                   - Change directory
  pwd                           - Show current directory
  mkdir <name>                  - Create directory

FILE COMMANDS:
  cat <file>                     - View text file
  rm <file>                      - Delete file
  mv <src> <dst>                 - Move/rename file
  cp <src> <dst>                 - Copy file

ENCRYPTION COMMANDS (.ezlock format):
  enc <file>                     - Encrypt (account) → file.ezlock
  enc -p <file>                   - Encrypt with password → file.ezlock
  enc -r <file>                   - Encrypt with random name → .ezlock
  dec <file.ezlock>               - Decrypt (account) → original
  dec -p <file.ezlock>             - Decrypt with password → original
  preview <file.ezlock>            - Preview encrypted file
  edit <file.ezlock>               - Secure edit encrypted file

FOLDER SECURITY COMMANDS:
  secure <folder>                 - Secure a folder
  unsecure <folder>               - Remove folder security
  folders                         - List secure folders

SYSTEM COMMANDS:
  clear                         - Clear screen
  history                       - Show command history
  memwipe                       - Wipe memory
  gui                           - Launch GUI
  help                          - Show this help
  exit                          - Exit

EXAMPLES:
  > register
  > login
  > enc secret.txt              → secret.txt.ezlock
  > enc -p "mypass" doc.pdf      → doc.pdf.ezlock
  > dec secret.txt.ezlock        → secret.txt
  > dec -p "mypass" doc.pdf.ezlock → doc.pdf
  > preview file.ezlock
  > edit file.ezlock
  > secure ./Documents
  > folders
  > license
  > support
═══════════════════════════════════════════════════
"""
        print(help_text)
    
    def clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print header"""
        if self.core.current_user:
            print(f"\nUser: {self.core.current_user} | Dir: {self.core.current_dir} | Format: .ezlock")
        else:
            print(f"\nNot logged in | Dir: {self.core.current_dir}")
        print("─" * 50)
    
    def run(self):
        """Run CLI interface"""
        self.clear_screen()
        print("\nEzLock V1.0.0 - Type 'help' for commands")
        print("=" * 50)
        
        while self.running:
            try:
                self.print_header()
                cmd = input("> ").strip()
                
                if not cmd:
                    continue
                
                self.history.append(cmd)
                parts = cmd.split()
                command = parts[0].lower()
                
                if command == 'help':
                    self.print_help()
                
                elif command == 'gui':
                    if TKINTER_AVAILABLE:
                        print("Launching GUI...")
                        gui = EzLockGUI(self.core)
                        gui.run()
                    else:
                        print("[-] Tkinter not available!")
                
                elif command in ['exit', 'quit']:
                    self.core.wipe_memory()
                    self.core.cleanup_all_temp_files()
                    print("Goodbye!")
                    self.running = False
                
                elif command in ['clear', 'cls']:
                    self.clear_screen()
                
                elif command == 'history':
                    for i, h in enumerate(self.history[-20:], 1):
                        print(f"{i:3}  {h}")
                
                elif command == 'memwipe':
                    success, message = self.core.wipe_memory()
                    print(message)
                
                elif command == 'license':
                    print(self.core.show_license())
                
                elif command == 'support':
                    print(self.core.show_support())
                
                elif command == 'guide':
                    print(self.core.show_user_guide())
                
                elif command == 'register':
                    if self.core.current_user:
                        print("[-] Please logout first!")
                        continue
                    
                    username = input("Username: ").strip()
                    password = getpass.getpass("Password: ")
                    confirm = getpass.getpass("Confirm: ")
                    
                    if password != confirm:
                        print("[-] Passwords don't match!")
                        continue
                    
                    success, message = self.core.register(username, password)
                    print(message)
                
                elif command == 'login':
                    if self.core.current_user:
                        print("[-] Already logged in!")
                        continue
                    
                    username = input("Username: ").strip()
                    password = getpass.getpass("Password: ")
                    
                    success, message = self.core.login(username, password)
                    print(message)
                
                elif command == 'logout':
                    if not self.core.current_user:
                        print("[-] Not logged in!")
                        continue
                    
                    success, message = self.core.logout()
                    print(message)
                
                elif command == 'whoami':
                    if self.core.current_user:
                        print(f"User: {self.core.current_user}")
                    else:
                        print("Not logged in")
                
                elif command == 'users':
                    if self.core.users:
                        print("\nRegistered Users:")
                        for user in self.core.users:
                            last = self.core.users[user].get('last_login', 'Never')
                            if last != 'Never':
                                last = datetime.fromtimestamp(last).strftime('%Y-%m-%d %H:%M')
                            print(f"  - {user} (Last login: {last})")
                    else:
                        print("No users registered.")
                
                elif command == 'pwd':
                    print(self.core.current_dir)
                
                elif command == 'ls':
                    success, files = self.core.list_files()
                    if success:
                        print()
                        for icon_img, name, size, ftype, is_secure in files:
                            try:
                                file_path = Path(self.core.current_dir) / name
                                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                                modified = mtime.strftime('%Y-%m-%d %H:%M')
                            except:
                                modified = ''
                            
                            # Show icon as text in CLI
                            if is_secure:
                                icon = '[SECURE]'
                            elif os.path.isdir(file_path):
                                icon = '[DIR]'
                            elif name.endswith('.ezlock'):
                                icon = '[EZLOCK]'
                            else:
                                ext = os.path.splitext(name)[1].lower()
                                if ext in self.core.streaming_formats:
                                    icon = '[STREAM]'
                                elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', '.webp']:
                                    icon = '[IMG]'
                                elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']:
                                    icon = '[VID]'
                                elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
                                    icon = '[AUD]'
                                elif ext in ['.pdf']:
                                    icon = '[PDF]'
                                elif ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                                    icon = '[DOC]'
                                elif ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml']:
                                    icon = '[TXT]'
                                elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
                                    icon = '[ARC]'
                                elif ext in ['.exe', '.msi', '.sh', '.bat']:
                                    icon = '[EXE]'
                                else:
                                    icon = '[FILE]'
                            
                            print(f"{icon}  {name:<30} {size:>10}  {modified}")
                    else:
                        print(f"[-] {files}")
                
                elif command == 'cd':
                    if len(parts) < 2:
                        success, message = self.core.change_directory('..')
                    else:
                        success, message = self.core.change_directory(parts[1])
                    print(message)
                
                elif command == 'mkdir':
                    if len(parts) < 2:
                        print("[-] Usage: mkdir <name>")
                        continue
                    
                    try:
                        os.mkdir(parts[1])
                        print(f"[+] Created: {parts[1]}")
                    except Exception as e:
                        print(f"[-] Error: {e}")
                
                elif command == 'cat':
                    if len(parts) < 2:
                        print("[-] Usage: cat <file>")
                        continue
                    
                    try:
                        with open(parts[1], 'r') as f:
                            print(f.read())
                    except Exception as e:
                        print(f"[-] Error: {e}")
                
                elif command == 'rm':
                    if len(parts) < 2:
                        print("[-] Usage: rm <file>")
                        continue
                    
                    try:
                        os.remove(parts[1])
                        print(f"[+] Deleted: {parts[1]}")
                    except Exception as e:
                        print(f"[-] Error: {e}")
                
                elif command == 'mv':
                    if len(parts) < 3:
                        print("[-] Usage: mv <src> <dst>")
                        continue
                    
                    try:
                        os.rename(parts[1], parts[2])
                        print(f"[+] Moved: {parts[1]} → {parts[2]}")
                    except Exception as e:
                        print(f"[-] Error: {e}")
                
                elif command == 'cp':
                    if len(parts) < 3:
                        print("[-] Usage: cp <src> <dst>")
                        continue
                    
                    try:
                        shutil.copy2(parts[1], parts[2])
                        print(f"[+] Copied: {parts[1]} → {parts[2]}")
                    except Exception as e:
                        print(f"[-] Error: {e}")
                
                elif command == 'secure':
                    if len(parts) < 2:
                        print("[-] Usage: secure <folder>")
                        continue
                    
                    folder = os.path.abspath(parts[1])
                    if not os.path.exists(folder):
                        print("[-] Folder not found!")
                        continue
                    
                    if not os.path.isdir(folder):
                        print("[-] Not a folder!")
                        continue
                    
                    print("Options:")
                    print("1. Include subfolders (default: yes)")
                    print("2. Use password protection (default: no)")
                    
                    sub = input("Include subfolders? (y/n): ").lower() == 'y'
                    use_pw = input("Use password? (y/n): ").lower() == 'y'
                    
                    password = None
                    if use_pw:
                        password = getpass.getpass("Password: ")
                        confirm = getpass.getpass("Confirm: ")
                        if password != confirm:
                            print("[-] Passwords don't match!")
                            continue
                    
                    success, message = self.core.start_folder_watching(folder, sub, password)
                    print(message)
                
                elif command == 'unsecure':
                    if len(parts) < 2:
                        print("[-] Usage: unsecure <folder>")
                        continue
                    
                    folder = os.path.abspath(parts[1])
                    success, message = self.core.stop_folder_watching(folder)
                    print(message)
                
                elif command == 'folders':
                    folders = self.core.get_secure_folders()
                    if not folders:
                        print("No secure folders configured")
                    else:
                        print("\nSECURE FOLDERS:")
                        for folder in folders:
                            sub = " (with subfolders)" if folder['include_subfolders'] else ""
                            pw = " [Password]" if folder['has_password'] else ""
                            start = datetime.fromtimestamp(folder['start_time']).strftime('%Y-%m-%d %H:%M')
                            print(f"  - {folder['path']}{sub}{pw} - since {start}")
                
                elif command == 'enc':
                    if len(parts) < 2:
                        print("[-] Usage: enc [options] <file>")
                        continue
                    
                    password = None
                    random_name = False
                    filepath = None
                    
                    i = 1
                    while i < len(parts):
                        if parts[i] == '-p':
                            if i + 1 < len(parts) and not parts[i+1].startswith('-'):
                                password = parts[i + 1]
                                i += 2
                            else:
                                password = getpass.getpass("Password: ")
                                i += 1
                        elif parts[i] == '-r':
                            random_name = True
                            i += 1
                        else:
                            filepath = parts[i]
                            i += 1
                    
                    if not filepath:
                        print("[-] No file specified!")
                        continue
                    
                    # Check for streaming formats
                    ext = os.path.splitext(filepath)[1].lower()
                    if ext in self.core.streaming_formats:
                        print(f"[-] Streaming format {ext} cannot be encrypted!")
                        continue
                    
                    success, message = self.core.encrypt_file(
                        filepath,
                        password=password,
                        random_name=random_name
                    )
                    print(message)
                
                elif command == 'dec':
                    if len(parts) < 2:
                        print("[-] Usage: dec [options] <file>")
                        continue
                    
                    password = None
                    filepath = None
                    
                    i = 1
                    while i < len(parts):
                        if parts[i] == '-p':
                            if i + 1 < len(parts) and not parts[i+1].startswith('-'):
                                password = parts[i + 1]
                                i += 2
                            else:
                                password = getpass.getpass("Password: ")
                                i += 1
                        else:
                            filepath = parts[i]
                            i += 1
                    
                    if not filepath:
                        print("[-] No file specified!")
                        continue
                    
                    if not filepath.endswith('.ezlock'):
                        print("[-] Expected .ezlock file!")
                        continue
                    
                    success, message, data = self.core.decrypt_file(
                        filepath,
                        password=password
                    )
                    print(message)
                
                elif command == 'edit':
                    if len(parts) < 2:
                        print("[-] Usage: edit <file.ezlock>")
                        continue
                    
                    filepath = parts[1]
                    
                    if not filepath.endswith('.ezlock'):
                        print("[-] Expected .ezlock file!")
                        continue
                    
                    password = None
                    if not self.core.current_user:
                        password = getpass.getpass("Password: ")
                    
                    success, message, temp_path = self.core.secure_edit_start(filepath, password)
                    
                    if not success:
                        print(message)
                        continue
                    
                    print(f"Opening file for editing...")
                    
                    # Open with default application
                    try:
                        if sys.platform == 'win32':
                            import subprocess
                            subprocess.Popen([temp_path], shell=True)
                        elif sys.platform == 'darwin':
                            subprocess.run(['open', temp_path])
                        else:
                            subprocess.run(['xdg-open', temp_path])
                    except Exception as e:
                        print(f"[-] Could not open file: {e}")
                        self.core.secure_edit_cancel(temp_path)
                        continue
                    
                    print("\nFile opened for editing.")
                    print("Options:")
                    print("1. Save and re-encrypt")
                    print("2. Discard changes")
                    
                    choice = input("Choice (1/2): ").strip()
                    
                    if choice == '1':
                        success, message = self.core.secure_edit_save(temp_path)
                        print(message)
                    else:
                        success, message = self.core.secure_edit_cancel(temp_path)
                        print(message)
                
                elif command == 'preview':
                    if len(parts) < 2:
                        print("[-] Usage: preview [options] <file.ezlock>")
                        continue
                    
                    password = None
                    filepath = None
                    
                    i = 1
                    while i < len(parts):
                        if parts[i] == '-p':
                            if i + 1 < len(parts) and not parts[i+1].startswith('-'):
                                password = parts[i + 1]
                                i += 2
                            else:
                                password = getpass.getpass("Password: ")
                                i += 1
                        else:
                            filepath = parts[i]
                            i += 1
                    
                    if not filepath:
                        print("[-] No file specified!")
                        continue
                    
                    if not filepath.endswith('.ezlock'):
                        print("[-] Expected .ezlock file!")
                        continue
                    
                    success, message, data = self.core.preview_file(filepath, password)
                    
                    if success:
                        decrypted_data, metadata = data
                        print(f"\nSECURE PREVIEW (In Memory Only)")
                        print("=" * 50)
                        print(f"File: {os.path.basename(filepath)}")
                        print(f"Original: {metadata.get('original_name', 'unknown')}")
                        print(f"Size: {len(decrypted_data)} bytes")
                        print(f"Type: {self.core.get_file_type(decrypted_data)}")
                        if metadata.get('key_source') == 'password':
                            print(f"Mode: Password Decryption")
                        else:
                            print(f"Mode: Account Decryption")
                        print("=" * 50)
                        
                        try:
                            if self.core.get_file_type(decrypted_data).startswith('text'):
                                print(decrypted_data.decode('utf-8', errors='replace')[:2000])
                                if len(decrypted_data) > 2000:
                                    print("\n... (preview truncated)")
                            else:
                                print("[BINARY FILE]")
                                print(f"First 64 bytes: {decrypted_data[:64].hex()}")
                        except:
                            print("[CANNOT PREVIEW]")
                    else:
                        print(message)
                
                else:
                    print(f"[-] Unknown command: {command}")
                    print("Type 'help' for available commands")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                self.core.wipe_memory()
                self.core.cleanup_all_temp_files()
                break
            except Exception as e:
                print(f"[-] Error: {e}")


def main():
    """Main entry point"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Create core instance
    core = EzLockCore()
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] in ['--gui', '-g', 'gui']:
        if TKINTER_AVAILABLE:
            gui = EzLockGUI(core)
            gui.run()
        else:
            print("[-] Tkinter not available! Using CLI mode.")
            cli = EzLockCLI(core)
            cli.run()
    else:
        cli = EzLockCLI(core)
        cli.run()


if __name__ == "__main__":
    # Check for watchdog
    try:
        import watchdog
    except ImportError:
        print("Installing watchdog for folder security...")
        os.system("pip install watchdog")
        print("Watchdog installed. Please restart EzLock.")
        sys.exit(0)
    
    # Check for required audio/video libraries
    if not PYDUB_AVAILABLE:
        print("For better audio support, install: pip install pydub numpy")
    
    if not CV2_AVAILABLE:
        print("For video support, install: pip install opencv-python")

    main()
