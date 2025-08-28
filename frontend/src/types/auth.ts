// types for login / register

export interface LoginPayload {
  username: string;
  password: string;
}

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

// reply upon login
export interface TokenResponse {
  access_token: string;
  token_type: string;
}