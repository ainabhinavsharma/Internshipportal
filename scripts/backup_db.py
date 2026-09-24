#!/usr/bin/env python3
"""
scripts/backup_db.py - Automated, WAL-Safe SQLite Backup Utility
Fulfills SAFE-001 requirements of DBERT_PORTAL_NEXT_PHASE_MASTER_PLAN.md

Features:
- Online, non-blocking backup via sqlite3.Connection.backup() API (WAL-safe)
- Canonical timestamp format: backups/dbert_YYYY_MM_DD_HH_MM_SS.db
- Computes SHA-256 integrity hash (.sha256 companion file)
- Verifies PRAGMA integrity_check on the destination backup
- Logs audit entry to backups/backup_manifest.json
"""
import os
import sys
import sqlite3
import hashlib
import json
import argparse
from datetime import datetime

# Add root directory to sys.path to read .env
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, ".env"))
except ImportError:
    pass

BACKUPS_DIR = os.path.join(BASE_DIR, "backups")

def resolve_source_db():
    env_db = os.environ.get("DB_FILE")
    if env_db:
        # If relative path, join with BASE_DIR
        if not os.path.isabs(env_db):
            return os.path.join(BASE_DIR, env_db)
        return env_db
    # Default fallbacks
    for candidate in ("internship.db", "internship_live.db"):
        path = os.path.join(BASE_DIR, candidate)
        if os.path.exists(path):
            return path
    return os.path.join(BASE_DIR, "internship.db")

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def create_backup(reason="manual"):
    os.makedirs(BACKUPS_DIR, exist_ok=True)
    source_db = resolve_source_db()
    
    if not os.path.exists(source_db):
        raise FileNotFoundError(f"Source database file not found at: {source_db}")
        
    now = datetime.now()
    timestamp_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    backup_filename = f"dbert_{timestamp_str}.db"
    backup_path = os.path.join(BACKUPS_DIR, backup_filename)
    sha_path = f"{backup_path}.sha256"
    
    print(f"[*] Initiating WAL-safe online backup...")
    print(f"    Source: {source_db} ({os.path.getsize(source_db):,} bytes)")
    print(f"    Target: {backup_path}")
    print(f"    Reason: {reason}")
    
    # Use SQLite's online backup API to ensure 100% transactional consistency even during concurrent writes
    src_conn = sqlite3.connect(source_db, timeout=30)
    dst_conn = sqlite3.connect(backup_path)
    
    try:
        with dst_conn:
            src_conn.backup(dst_conn, pages=100, sleep=0.01)
    finally:
        dst_conn.close()
        src_conn.close()
        
    # Check integrity of the generated backup
    verify_conn = sqlite3.connect(backup_path)
    try:
        integrity = verify_conn.execute("PRAGMA integrity_check").fetchall()
        if integrity != [('ok',)]:
            raise RuntimeError(f"Integrity check failed on backup: {integrity}")
        table_count = verify_conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    finally:
        verify_conn.close()
        
    # Compute SHA-256
    sha256_hash = compute_sha256(backup_path)
    with open(sha_path, "w", encoding="utf-8") as f:
        f.write(f"{sha256_hash}  {backup_filename}\n")
        
    backup_size = os.path.getsize(backup_path)
    print(f"[+] Backup successfully created and verified!")
    print(f"    Size: {backup_size:,} bytes")
    print(f"    SHA-256: {sha256_hash}")
    print(f"    Tables: {table_count}")
    
    # Update manifest
    manifest_path = os.path.join(BACKUPS_DIR, "backup_manifest.json")
    manifest = []
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = []
            
    manifest.append({
        "timestamp": now.isoformat(),
        "filename": backup_filename,
        "path": os.path.relpath(backup_path, BASE_DIR),
        "source": os.path.relpath(source_db, BASE_DIR),
        "size_bytes": backup_size,
        "sha256": sha256_hash,
        "tables": table_count,
        "reason": reason,
        "status": "VERIFIED_OK"
    })
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    return backup_path, sha256_hash

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a verified, timestamped SQLite database backup.")
    parser.add_argument("--reason", default="manual", choices=["daily", "pre-release", "pre-migration", "manual", "emergency"],
                        help="Reason for creating the backup.")
    args = parser.parse_args()
    
    try:
        create_backup(args.reason)
    except Exception as e:
        print(f"[!] Backup failed: {e}", file=sys.stderr)
        sys.exit(1)
