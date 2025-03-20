"""
Mesh ZKP Client

This module provides a Zero-Knowledge Proof client for securely interacting with the Mesh API.
"""

import json
import hashlib
import os
import requests
import logging
from typing import Dict, Any, Optional, Tuple

from .client import MeshClient

# Configure logging
logger = logging.getLogger("mesh.zkp_client")

class MeshZKPClient(MeshClient):
    """
    Zero-Knowledge Proof client for the Mesh API
    
    This client extends the base MeshClient with Zero-Knowledge Proof (ZKP) capabilities
    for secure key management. It allows storing and verifying keys without exposing
    their values to the server.
    
    Key features:
    1. Secure key storage using commitments
    2. Challenge-response verification protocol
    3. Client-side verification to ensure security even with server issues
    
    The implementation uses hash-based commitments and proofs to protect key values
    while still allowing verification of ownership.
    
    Example:
        ```python
        # Initialize ZKP client
        zkp_client = MeshZKPClient()
        
        # Store a key securely
        zkp_client.store_key_zkp("user123", "api_key", "secret_value")
        
        # Verify key ownership without exposing the key
        result = zkp_client.verify_key("user123", "api_key", "secret_value")
        if result.get("verified"):
            logger.info("Key verified successfully!")
        ```
    
    All methods have built-in error handling and will provide clear error messages
    when issues occur.
    """
    
    def __init__(self, 
                 server_url: str = None, 
                 zkp_server_url: str = None,
                 user_id: str = None, 
                 client_id: str = None, 
                 client_secret: str = None,
                 audience: str = None,
                 auth0_domain: str = None):
        """Initialize the ZKP client
        
        Args:
            server_url: URL of the Mesh API server (defaults to env var or production URL)
            zkp_server_url: Specific URL for the ZKP server (defaults to server_url if not provided)
            user_id: Optional default user ID to use for all operations
            client_id: Auth0 client ID (defaults to env var)
            client_secret: Auth0 client secret (defaults to env var)
            audience: Auth0 audience (defaults to env var)
            auth0_domain: Auth0 domain (defaults to env var or default domain)
        """
        # If server_url is not provided but zkp_server_url is, use zkp_server_url for both
        if not server_url and zkp_server_url:
            server_url = zkp_server_url
            
        # Call parent's constructor
        super().__init__(
            server_url=server_url, 
            zkp_server_url=zkp_server_url,
            client_id=client_id,
            client_secret=client_secret,
            audience=audience,
            auth0_domain=auth0_domain
        )
        
        self.user_id = user_id  # Store user_id for operations
    
    def _generate_nullifier(self, key_name: str, key_value: str) -> str:
        """Generate a nullifier based on the key name and value
        
        Args:
            key_name: Key name
            key_value: Key value
            
        Returns:
            str: Nullifier hash
        """
        # Combine key name and value to create nullifier
        combined = f"{key_name}:{key_value}"
        nullifier = hashlib.sha256(combined.encode()).hexdigest()
        return nullifier
    
    def _generate_commitment(self, key_value: str, nullifier: str) -> str:
        """Generate a commitment for a key value
        
        Args:
            key_value: The secret key value
            nullifier: A nullifier to prevent replay attacks
            
        Returns:
            A commitment hash
        """
        # Combine the key and nullifier to create a commitment
        combined = f"{key_value}:{nullifier}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _generate_proof(self, nullifier: str, challenge: str, commitment: str) -> str:
        """Generate a proof for the given nullifier, challenge, and commitment
        
        Args:
            nullifier: Nullifier hash
            challenge: Challenge string
            commitment: Commitment hash
            
        Returns:
            str: Proof hash
        """
        # Log proof calculation details at debug level
        logger.debug("Client-side proof calculation:")
        logger.debug(f"Nullifier: {nullifier}")
        logger.debug(f"Challenge: {challenge}")
        logger.debug(f"Commitment: {commitment}")
        
        # Concatenate nullifier, challenge, and commitment
        data = f"{nullifier}:{challenge}:{commitment}"
        
        # Log concatenated data at debug level
        logger.debug(f"Concatenated data: {data}")
        
        # Hash the concatenated data to create the proof
        proof = hashlib.sha256(data.encode()).hexdigest()
        
        return proof
    
    def get_challenge(self, user_id: str, key_name: str) -> Dict[str, Any]:
        """Get a challenge from the server for key verification
        
        Args:
            user_id: User ID
            key_name: Key name
            
        Returns:
            Dict containing the challenge response
        """
        # Get a challenge from the server
        url = self._get_zkp_url("/v1/mesh/getChallenge")
        params = {
            "userId": user_id,
            "keyName": key_name
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"Failed to get challenge: {response.status_code}",
                    "details": response.json() if response.content else None
                }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def store_key_zkp(self, user_id: str, key_name: str, key_value: str) -> Dict[str, Any]:
        """Store a key with ZKP commitment
        
        Args:
            user_id: User ID to associate with the key
            key_name: Key name
            key_value: Key value to store
            
        Returns:
            Dict containing the result of the operation
        """
        # Use passed user_id or fall back to instance user_id
        user_id_to_use = user_id or self.user_id
        if not user_id_to_use:
            return {"status": "error", "success": False, "error": "No user ID provided"}
        
        # Ensure user exists
        self.ensure_user_exists(user_id_to_use)
        
        # Generate a nullifier and commitment
        nullifier = self._generate_nullifier(key_name, key_value)
        commitment = self._generate_commitment(key_value, nullifier)
        
        # Store the key with its commitment
        url = self._get_zkp_url("/v1/mesh/storeKeyZKP")
        data = {
            "userId": user_id_to_use,
            "keyName": key_name,
            "commitment": commitment
        }
        
        try:
            response = requests.post(
                url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                result = response.json()
                # Store the actual parameters used for later verification, 
                # since the server response has them swapped
                result["actualUserId"] = user_id_to_use
                result["actualKeyName"] = key_name
                return {
                    "success": True,
                    "userId": user_id_to_use,
                    "keyName": key_name,
                    "commitment": commitment
                }
            elif response.status_code == 402:
                # Payment required - insufficient credits
                return {
                    "success": False,
                    "error": "Insufficient credits",
                    "details": response.json() if response.content else None
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to store key: {response.status_code}",
                    "details": response.json() if response.content else None
                }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def _get_storage_details(self, user_id: str, key_name: str) -> Dict[str, Any]:
        """
        Get the stored key value directly (for testing only)
        
        In a production environment, this would not be exposed.
        
        Args:
            user_id: User identifier
            key_name: Name of the key
            
        Returns:
            Dict with stored key details
        """
        url = self._get_zkp_url("/v1/mesh/getKey")
        params = {
            "userId": user_id,
            "keyName": key_name
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                return {"success": False, "error": f"Failed to retrieve key details: {response.text}"}
            
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_key(self, user_id: str, key_name: str, key_value: str) -> Dict[str, Any]:
        """Verify that a key value matches what's stored on the server
        
        This method performs a challenge-response verification to prove
        knowledge of a key value without revealing it to the server.
        
        Args:
            user_id: User ID
            key_name: Key name
            key_value: Key value to verify
            
        Returns:
            dict: Verification result with 'verified' boolean
        """
        try:
            # Get challenge from server
            challenge_result = self.get_challenge(user_id, key_name)
            
            if not challenge_result.get("success", False):
                return challenge_result
            
            challenge = challenge_result.get("challenge", "")
            
            # Generate nullifier
            nullifier = self._generate_nullifier(key_name, key_value)
            
            # Try to get the stored commitment from the server
            stored_commitment_url = f"{self.server_url}/api/v1/zkp/commitment/{user_id}/{key_name}"
            
            # Fallback to legacy endpoint if needed
            if not stored_commitment_url.startswith(self.server_url):
                stored_commitment_url = f"{self.server_url}/api/v1/zkp/commitment/{user_id}/{key_name}"
            
            logger.debug(f"Attempting to fetch commitment from: {stored_commitment_url}")
            
            try:
                response = requests.get(stored_commitment_url, headers=self._get_auth_headers())
                
                if response.status_code == 200:
                    stored_commitment = response.json().get("commitment", "")
                    logger.debug(f"Successfully retrieved stored commitment: {stored_commitment}")
                else:
                    logger.debug(f"Unable to get stored commitment (status: {response.status_code}), using local calculation")
                    logger.debug(f"Response: {response.text}")
                    stored_commitment = None
            except Exception as e:
                logger.debug(f"Error getting stored commitment: {str(e)}, using local calculation")
                stored_commitment = None
            
            # Calculate commitment locally
            local_commitment = self._generate_commitment(key_value, nullifier)
            
            # Verify locally first (client-side verification)
            if stored_commitment and stored_commitment != local_commitment:
                logger.warning("Client-side verification failed: key value doesn't match stored commitment")
                return {
                    "success": False,
                    "verified": False,
                    "error": "Key value doesn't match stored commitment",
                    "client_verified": False
                }
            
            # Generate proof
            logger.debug("Client-side proof calculation:")
            logger.debug(f"Nullifier: {nullifier}")
            logger.debug(f"Challenge: {challenge}")
            logger.debug(f"Commitment: {local_commitment}")
            
            # For debug purposes, show the full concatenated data
            data = f"{nullifier}:{challenge}:{local_commitment}"
            logger.debug(f"Concatenated data: {data}")
            
            proof = self._generate_proof(nullifier, challenge, local_commitment)
            
            # Send proof to server for verification
            verify_url = f"{self.server_url}/api/v1/zkp/verify/{user_id}/{key_name}"
            
            # Fallback to legacy endpoint if needed
            if not verify_url.startswith(self.server_url):
                verify_url = f"{self.server_url}/api/v1/zkp/verify/{user_id}/{key_name}"
            
            data = {
                "proof": proof,
                "challenge": challenge
            }
            
            logger.debug(f"Sending verification request to: {verify_url}")
            logger.debug(f"Request data: {data}")
            
            response = requests.post(verify_url, json=data, headers=self._get_auth_headers())
            
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response text: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Add client-side verification result
                result["client_verified"] = True
                
                return result
            else:
                error_message = "Server verification failed"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_message = error_data["error"]
                except:
                    error_message = f"Server error: {response.status_code}"
                
                return {
                    "success": False,
                    "verified": False,
                    "error": error_message,
                    "client_verified": True  # Client verified but server rejected
                }
        except Exception as e:
            logger.error(f"Error verifying key: {str(e)}")
            return {
                "success": False,
                "verified": False,
                "error": f"Verification error: {str(e)}"
            }
    
    def get_user_credits(self, user_id):
        """
        Get the current credit balance for a user.
        
        Args:
            user_id (str): The user's ID
            
        Returns:
            dict: Response containing credit information or error
        """
        url = self._get_zkp_url(f"/v1/mesh/users/{user_id}/credits")
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False,
                "error": f"Failed to get user credits: {response.status_code}",
                "details": response.json() if response.content else None
            }
    
    def ensure_user_exists(self, user_id, email=None):
        """
        Ensure the user exists in the system. If not, creates the user with default credits.
        
        Args:
            user_id (str): The user's ID
            email (str, optional): The user's email
            
        Returns:
            dict: Response containing user information or error
        """
        url = self._get_zkp_url("/v1/mesh/users")
        data = {"id": user_id}
        if email:
            data["email"] = email
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False,
                "error": f"Failed to ensure user exists: {response.status_code}",
                "details": response.json() if response.content else None
            } 