import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, CircularProgress, Paper } from '@mui/material';
import axios from 'axios';

function App() {
  const [apiState, setApiState] = useState({
    loading: true,
    status: null,
    error: null
  });

  useEffect(() => {
    // Verificação do status da API
    const checkApiStatus = async () => {
      try {
        const response = await axios.get('/health');
        setApiState({
          loading: false,
          status: response.data,
          error: null
        });
      } catch (err) {
        console.error('Erro ao conectar com a API:', err);
        setApiState({
          loading: false,
          status: null,
          error: 'Não foi possível conectar com a API. Verifique se o backend está em execução.'
        });
      }
    };

    checkApiStatus();
  }, []);

  const { loading, status, error } = apiState;

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          JurIA - Assistente Jurídico com IA
        </Typography>
        
        <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
          <Typography variant="h5" component="h2" gutterBottom>
            Status do Sistema
          </Typography>
          
          {loading ? (
            <Box display="flex" justifyContent="center" my={4}>
              <CircularProgress />
            </Box>
          ) : error ? (
            <Typography color="error">{error}</Typography>
          ) : (
            <Box>
              <Typography variant="body1">
                Status da API: {status?.status === 'healthy' ? 
                  <span style={{ color: 'green' }}>Operacional</span> : 
                  <span style={{ color: 'red' }}>Indisponível</span>}
              </Typography>
              <Typography variant="body1" mt={2}>
                O projeto JurIA está em desenvolvimento. Em breve teremos mais funcionalidades disponíveis.
              </Typography>
            </Box>
          )}
        </Paper>
      </Box>
    </Container>
  );
}

export default App; 