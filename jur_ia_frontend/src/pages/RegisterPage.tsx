import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { 
  Alert,
  Box, 
  Button, 
  CircularProgress, 
  Container, 
  Paper, 
  TextField, 
  Typography 
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { RegisterData } from '../types/auth';

// Schema de validação
const schema = yup.object().shape({
  nome: yup.string().required('Nome é obrigatório'),
  email: yup.string().email('E-mail inválido').required('E-mail é obrigatório'),
  password: yup.string()
    .required('Senha é obrigatória')
    .min(8, 'A senha deve ter pelo menos 8 caracteres'),
  confirmPassword: yup.string()
    .oneOf([yup.ref('password')], 'As senhas não conferem')
    .required('Confirmação de senha é obrigatória'),
});

interface RegisterFormData extends RegisterData {
  confirmPassword: string;
}

const RegisterPage: React.FC = () => {
  const { register: registerUser, isAuthenticated, loading, error, clearError } = useAuth();
  const navigate = useNavigate();
  
  const { register, handleSubmit, formState: { errors } } = useForm<RegisterFormData>({
    resolver: yupResolver(schema),
  });

  // Se já estiver autenticado, redireciona para a página de consulta
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/consulta');
    }
  }, [isAuthenticated, navigate]);

  const onSubmit = async (data: RegisterFormData) => {
    const { nome, email, password } = data;
    await registerUser({ nome, email, password });
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography variant="h4" component="h1" align="center" gutterBottom>
          Cadastro
        </Typography>
        <Typography variant="body1" align="center" sx={{ mb: 4 }}>
          Crie sua conta para acessar o JurIA
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={clearError}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
          <TextField
            margin="normal"
            required
            fullWidth
            id="nome"
            label="Nome completo"
            autoComplete="name"
            autoFocus
            {...register('nome')}
            error={!!errors.nome}
            helperText={errors.nome?.message}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="E-mail"
            autoComplete="email"
            {...register('email')}
            error={!!errors.email}
            helperText={errors.email?.message}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="password"
            label="Senha"
            type="password"
            autoComplete="new-password"
            {...register('password')}
            error={!!errors.password}
            helperText={errors.password?.message}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="confirmPassword"
            label="Confirmar senha"
            type="password"
            autoComplete="new-password"
            {...register('confirmPassword')}
            error={!!errors.confirmPassword}
            helperText={errors.confirmPassword?.message}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Cadastrar'}
          </Button>
          <Box textAlign="center">
            <Typography variant="body2">
              Já tem uma conta?{' '}
              <Link to="/login" style={{ textDecoration: 'none' }}>
                Faça login
              </Link>
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default RegisterPage; 