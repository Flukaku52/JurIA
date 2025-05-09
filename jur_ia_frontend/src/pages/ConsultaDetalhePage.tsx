import React, { useEffect, useState } from 'react';
import { 
  Alert,
  Box, 
  Button,
  Card,
  CardContent,
  CircularProgress, 
  Container, 
  Divider,
  Paper,
  Typography 
} from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { consultaService } from '../services/consultaService';
import { ConsultaResponse } from '../types/consulta';

const ConsultaDetalhePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [consulta, setConsulta] = useState<ConsultaResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const carregarConsulta = async () => {
      if (!id || isNaN(parseInt(id))) {
        setError('ID de consulta inválido');
        setLoading(false);
        return;
      }

      setLoading(true);
      try {
        const data = await consultaService.obterConsulta(parseInt(id));
        setConsulta(data);
        setError(null);
      } catch (err: any) {
        console.error('Erro ao carregar consulta:', err);
        setError(err.response?.data?.detail || 'Erro ao carregar detalhes da consulta');
      } finally {
        setLoading(false);
      }
    };

    carregarConsulta();
  }, [id]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md">
        <Alert 
          severity="error" 
          sx={{ mt: 4 }}
          action={
            <Button color="inherit" size="small" onClick={() => navigate(-1)}>
              Voltar
            </Button>
          }
        >
          {error}
        </Alert>
      </Container>
    );
  }

  if (!consulta) {
    return (
      <Container maxWidth="md">
        <Alert 
          severity="warning" 
          sx={{ mt: 4 }}
          action={
            <Button color="inherit" size="small" onClick={() => navigate(-1)}>
              Voltar
            </Button>
          }
        >
          Consulta não encontrada
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Button 
        variant="outlined" 
        onClick={() => navigate(-1)}
        sx={{ mb: 3, mt: 2 }}
      >
        Voltar ao histórico
      </Button>

      <Card variant="outlined" sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" component="h1" gutterBottom>
            Consulta Jurídica #{consulta.id}
          </Typography>
          
          <Divider sx={{ mb: 2 }} />
          
          <Typography variant="h6" gutterBottom>
            Pergunta:
          </Typography>
          <Paper elevation={0} sx={{ p: 2, bgcolor: 'grey.100', mb: 3 }}>
            <Typography variant="body1">
              {consulta.pergunta}
            </Typography>
          </Paper>
          
          {consulta.contexto && (
            <>
              <Typography variant="h6" gutterBottom>
                Contexto:
              </Typography>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'grey.100', mb: 3 }}>
                <Typography variant="body1">
                  {consulta.contexto}
                </Typography>
              </Paper>
            </>
          )}
          
          <Typography variant="h6" gutterBottom>
            Resposta:
          </Typography>
          <Paper 
            elevation={0} 
            sx={{ 
              p: 3, 
              bgcolor: 'primary.light', 
              color: 'primary.contrastText',
              whiteSpace: 'pre-line'
            }}
          >
            <Typography variant="body1">
              {consulta.resposta}
            </Typography>
          </Paper>
          
          <Box 
            display="flex" 
            justifyContent="space-between" 
            alignItems="center"
            mt={3}
          >
            <Typography variant="body2" color="textSecondary">
              Status: {consulta.status.toUpperCase()}
            </Typography>
            <Box>
              <Typography variant="body2" color="textSecondary">
                Criado em: {new Date(consulta.data_criacao).toLocaleString()}
              </Typography>
              {consulta.data_resposta && (
                <Typography variant="body2" color="textSecondary">
                  Respondido em: {new Date(consulta.data_resposta).toLocaleString()}
                </Typography>
              )}
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default ConsultaDetalhePage; 