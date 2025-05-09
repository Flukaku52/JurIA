import React, { useEffect, useState } from 'react';
import { 
  Alert,
  Box, 
  Button,
  Card,
  CardActions,
  CardContent,
  CircularProgress, 
  Container, 
  Divider,
  Grid,
  Typography 
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { consultaService } from '../services/consultaService';
import { ConsultaHistorico } from '../types/consulta';

const HistoricoPage: React.FC = () => {
  const [consultas, setConsultas] = useState<ConsultaHistorico[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const carregarConsultas = async () => {
      setLoading(true);
      try {
        const data = await consultaService.listarConsultas();
        setConsultas(data);
        setError(null);
      } catch (err: any) {
        console.error('Erro ao carregar consultas:', err);
        setError(err.response?.data?.detail || 'Erro ao carregar histórico de consultas');
      } finally {
        setLoading(false);
      }
    };

    carregarConsultas();
  }, []);

  const handleVerConsulta = (id: number) => {
    navigate(`/consulta/${id}`);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        Histórico de Consultas
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {consultas.length === 0 ? (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="textSecondary" gutterBottom>
            Você ainda não realizou nenhuma consulta
          </Typography>
          <Button 
            variant="contained" 
            color="primary" 
            sx={{ mt: 2 }}
            onClick={() => navigate('/consulta')}
          >
            Fazer uma consulta
          </Button>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {consultas.map((consulta) => (
            <Grid item xs={12} md={6} lg={4} key={consulta.id}>
              <Card variant="outlined">
                <CardContent>
                  <Typography 
                    variant="h6" 
                    noWrap 
                    title={consulta.pergunta}
                    sx={{ 
                      mb: 1,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                    }}
                  >
                    {consulta.pergunta}
                  </Typography>
                  <Typography color="textSecondary" variant="body2">
                    Data: {new Date(consulta.data_criacao).toLocaleDateString()}
                  </Typography>
                  <Divider sx={{ my: 1 }} />
                  <Box 
                    display="flex" 
                    justifyContent="space-between" 
                    alignItems="center"
                  >
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        bgcolor: 
                          consulta.status === 'respondida' ? 'success.light' : 
                          consulta.status === 'pendente' ? 'warning.light' : 'info.light',
                        color: 
                          consulta.status === 'respondida' ? 'success.contrastText' : 
                          consulta.status === 'pendente' ? 'warning.contrastText' : 'info.contrastText',
                        px: 1,
                        py: 0.5,
                        borderRadius: 1
                      }}
                    >
                      {consulta.status.toUpperCase()}
                    </Typography>
                    {consulta.data_resposta && (
                      <Typography variant="caption">
                        Respondido em: {new Date(consulta.data_resposta).toLocaleTimeString()}
                      </Typography>
                    )}
                  </Box>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    onClick={() => handleVerConsulta(consulta.id)}
                    variant="outlined"
                    fullWidth
                  >
                    Ver detalhes
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default HistoricoPage; 