from pydbmanager.config import Config

print("Database Configuration Loaded:")
print(f"SERVER: {Config.SERVER}")
print(f"DATABASE: {Config.DATABASE}")
print(f"USERNAME: {Config.USERNAME}")
print(f"PASSWORD: {'*' * len(Config.PASSWORD) if Config.PASSWORD else 'Not Set'}")
print(f"DRIVER: {Config.DRIVER}")
