import React from 'react';
import {
  Box,
  Button,
  Container,
  Grid,
  Paper,
  Typography,
} from '@mui/material';
import { Link } from 'react-router-dom';
import GavelIcon from '@mui/icons-material/Gavel';
import SearchIcon from '@mui/icons-material/Search';
import AssignmentIcon from '@mui/icons-material/Assignment';
import { useAuth } from '../contexts/AuthContext';

const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Box sx={{ flexGrow: 1, pb: 8 }}>
      {/* Hero Section */}
      <Paper 
        sx={{ 
          py: 8, 
          mb: 6, 
          bgcolor: 'primary.main', 
          color: 'primary.contrastText',
          borderRadius: 0 
        }} 
        elevation={0}
      >
        <Container maxWidth="md">
          <Typography variant="h2" component="h1" align="center" gutterBottom>
            JurIA
          </Typography>
          <Typography variant="h5" align="center" paragraph>
            Seu assistente jurídico com inteligência artificial
          </Typography>
          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
            <Button
              variant="contained"
              color="secondary"
              size="large"
              component={Link}
              to={isAuthenticated ? '/consulta' : '/login'}
              sx={{ px: 4, py: 1.5 }}
            >
              {isAuthenticated ? 'Nova Consulta' : 'Começar Agora'}
            </Button>
          </Box>
        </Container>
      </Paper>

      {/* Features */}
      <Container maxWidth="lg">
        <Typography variant="h4" component="h2" align="center" gutterBottom>
          Como a JurIA pode ajudar você
        </Typography>
        <Typography variant="subtitle1" align="center" paragraph sx={{ mb: 6 }}>
          Uma solução completa para suas dúvidas jurídicas
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 4, height: '100%' }} elevation={2}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
                <GavelIcon color="primary" sx={{ fontSize: 60, mb: 2 }} />
                <Typography variant="h5" component="h3" align="center" gutterBottom>
                  Consultas Jurídicas
                </Typography>
              </Box>
              <Typography variant="body1" align="center">
                Tire suas dúvidas jurídicas com respostas rápidas e precisas baseadas em legislação atualizada.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 4, height: '100%' }} elevation={2}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
                <SearchIcon color="primary" sx={{ fontSize: 60, mb: 2 }} />
                <Typography variant="h5" component="h3" align="center" gutterBottom>
                  Pesquisa de Jurisprudência
                </Typography>
              </Box>
              <Typography variant="body1" align="center">
                Encontre jurisprudências relevantes para seu caso com nossa ferramenta de busca inteligente.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 4, height: '100%' }} elevation={2}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
                <AssignmentIcon color="primary" sx={{ fontSize: 60, mb: 2 }} />
                <Typography variant="h5" component="h3" align="center" gutterBottom>
                  Histórico de Consultas
                </Typography>
              </Box>
              <Typography variant="body1" align="center">
                Acesse facilmente seu histórico de consultas anteriores para referência futura.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default HomePage; 