import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Paper,
  Alert,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import type { LoginCredentials } from '../types/auth';

// Schema de validação
const schema = yup.object({
  username: yup.string().required('Email é obrigatório').email('Email inválido'),
  password: yup.string().required('Senha é obrigatória'),
}).required();

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, error, loading, clearError } = useAuth();
  
  const { register, handleSubmit, formState: { errors } } = useForm<LoginCredentials>({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data: LoginCredentials) => {
    clearError();
    await login(data);
    // O redirecionamento será feito pelo AuthContext se o login for bem-sucedido
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography component="h1" variant="h5" align="center" gutterBottom>
            Login
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          
          <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Email"
              autoComplete="email"
              autoFocus
              {...register('username')}
              error={!!errors.username}
              helperText={errors.username?.message}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              id="password"
              label="Senha"
              type="password"
              autoComplete="current-password"
              {...register('password')}
              error={!!errors.password}
              helperText={errors.password?.message}
            />
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </Button>
            
            <Button
              fullWidth
              variant="text"
              onClick={() => navigate('/register')}
            >
              Não tem uma conta? Registre-se
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage; 