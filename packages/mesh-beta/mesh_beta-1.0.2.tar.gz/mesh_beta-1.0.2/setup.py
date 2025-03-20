from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import logging

# Configure logging
logger = logging.getLogger("mesh.setup")

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        try:
            # Only run auth flow if explicitly requested and not in CI/CD
            if os.environ.get('MESH_AUTO_AUTH') and not os.environ.get('CI'):
                logger.info("Running post-install authentication flow...")
                try:
                    from mesh.auth import authenticate_device_flow
                    
                    print("\n=== Mesh SDK Authentication Required ===")
                    print("A browser window will NOT be opened automatically.")
                    print("Please follow these steps:")
                    print("1. You will see a URL and a code displayed below")
                    print("2. Open the URL in any browser (can be on another device)")
                    print("3. Enter the code when prompted")
                    print("4. Complete the authentication process")
                    print("===========================================\n")
                    
                    # Use device code flow exclusively (doesn't require a local server)
                    token_data = authenticate_device_flow()
                    
                    if token_data:
                        logger.info("Authentication successful using device code flow.")
                        print("\n✅ Authentication successful! You can now use the Mesh SDK.")
                    else:
                        logger.warning("Authentication failed.")
                        print("\nAuthentication failed. Please run 'mesh-auth' manually after installation.")
                        print("If you're on a server without a browser, use: mesh-auth --headless")
                        print("Make sure your Auth0 application is configured for device code flow.")
                        print("See the README for configuration instructions.")
                except Exception as e:
                    logger.warning(f"Authentication failed: {e}")
                    print("\nAuthentication failed. Please run 'mesh-auth' manually after installation.")
                    print("If you're on a server without a browser, use: mesh-auth --headless")
                    print("Make sure your Auth0 application is configured for device code flow.")
                    print("See the README for configuration instructions.")
            else:
                logger.info("Skipping automatic authentication. Run 'mesh-auth' to authenticate manually.")
        except Exception as e:
            logger.warning(f"Post-install authentication failed: {e}")
            logger.info("You can authenticate later by running 'mesh-auth' from the command line")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mesh-beta",
    version="1.0.2",
    author="Mesh Team",
    author_email="support@meshsdk.io",
    description="Official Python SDK for the Mesh API - Secure key management and AI model access",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meshsdk/mesh-python",
    project_urls={
        "Documentation": "https://docs.meshsdk.io",
        "Source": "https://github.com/meshsdk/mesh-python",
        "Issues": "https://github.com/meshsdk/mesh-python/issues",
    },
    packages=find_packages(exclude=["tests*", "examples*", "docs*"]),
    install_requires=[
        "requests>=2.31.0",
        "keyring>=24.3.0",
        "cryptography>=42.0.0",
        "pyjwt>=2.8.0",
        "urllib3>=2.0.0",
        "certifi>=2024.2.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=24.0.0",
            "isort>=5.13.0",
            "mypy>=1.8.0",
            "types-requests>=2.31.0",
            "types-urllib3>=1.26.25"
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=2.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "mesh-auth=mesh.auth_cli:main",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="mesh, api, sdk, security, key management, zero knowledge proofs, ai, openai, anthropic",
) 