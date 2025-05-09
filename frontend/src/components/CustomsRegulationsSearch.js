import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Card,
  CardContent,
  CardActions,
  Divider,
  Grid,
  CircularProgress,
  Chip,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  Search as SearchIcon,
  Public as PublicIcon,
  LocalShipping as ShippingIcon,
  Assignment as AssignmentIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import axios from 'axios';

const CustomsRegulationsSearch = () => {
  const [searchParams, setSearchParams] = useState({
    country: '',
    product_code: '',
    regulation_type: ''
  });
  
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleSearch = async () => {
    if (!searchParams.country && !searchParams.product_code && !searchParams.regulation_type) {
      setError('Por favor, especifique pelo menos um critério de busca');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get('/api/international-law/customs', { 
        params: searchParams 
      });
      
      setResults(response.data);
    } catch (err) {
      console.error('Erro ao buscar regulamentações alfandegárias:', err);
      setError('Falha ao buscar informações. Por favor, tente novamente.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };
  
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        <ShippingIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        Políticas Alfandegárias
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth variant="outlined">
              <InputLabel>País</InputLabel>
              <Select
                name="country"
                value={searchParams.country}
                onChange={handleInputChange}
                label="País"
              >
                <MenuItem value="">Todos</MenuItem>
                <MenuItem value="singapore">Singapura</MenuItem>
                <MenuItem value="global">Global</MenuItem>
                <MenuItem value="eu">União Europeia</MenuItem>
                <MenuItem value="usa">Estados Unidos</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Código HS do Produto"
              name="product_code"
              value={searchParams.product_code}
              onChange={handleInputChange}
              placeholder="Ex: 8471.30"
              variant="outlined"
              helperText="Sistema Harmonizado de Designação"
            />
          </Grid>
          
          <Grid item xs={12} md={4}>
            <FormControl fullWidth variant="outlined">
              <InputLabel>Tipo de Regulamentação</InputLabel>
              <Select
                name="regulation_type"
                value={searchParams.regulation_type}
                onChange={handleInputChange}
                label="Tipo de Regulamentação"
              >
                <MenuItem value="">Todos</MenuItem>
                <MenuItem value="import">Importação</MenuItem>
                <MenuItem value="export">Exportação</MenuItem>
                <MenuItem value="tariff">Tarifas</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleSearch}
              startIcon={<SearchIcon />}
              disabled={loading}
            >
              {loading ? 'Buscando...' : 'Buscar Regulamentações'}
            </Button>
          </Grid>
        </Grid>
        
        {error && (
          <Typography color="error" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )}
      </Paper>
      
      {loading ? (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          {results.length > 0 ? (
            <Box>
              <Typography variant="h6" gutterBottom>
                Resultados ({results.length})
              </Typography>
              <Grid container spacing={2}>
                {results.map((result) => (
                  <Grid item xs={12} key={result.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <AssignmentIcon sx={{ mr: 1, color: 'primary.main' }} />
                            <Typography variant="h6">{result.title}</Typography>
                          </Box>
                          <Chip 
                            label={result.country === 'singapore' ? 'Singapura' : 
                                  result.country === 'global' ? 'Global' : 
                                  result.country === 'eu' ? 'União Europeia' :
                                  result.country === 'usa' ? 'Estados Unidos' :
                                  result.country}
                            color={result.country === 'singapore' ? 'primary' : 'default'}
                            size="small"
                          />
                        </Box>
                        
                        <Divider sx={{ mb: 2 }} />
                        
                        <Typography variant="body2" paragraph>
                          {result.content}
                        </Typography>
                        
                        <Grid container spacing={2}>
                          {result.hs_codes && result.hs_codes.length > 0 && (
                            <Grid item xs={12} md={6}>
                              <Typography variant="body2" fontWeight="medium">
                                Códigos HS Aplicáveis:
                              </Typography>
                              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                                {result.hs_codes.map((code, index) => (
                                  <Chip key={index} label={code} size="small" variant="outlined" />
                                ))}
                              </Box>
                            </Grid>
                          )}
                          
                          {result.tariff_rate !== null && (
                            <Grid item xs={12} md={6}>
                              <Typography variant="body2" fontWeight="medium">
                                Taxa de Tarifa:
                              </Typography>
                              <Typography variant="body2">
                                {result.tariff_rate ? `${(result.tariff_rate * 100).toFixed(2)}%` : 'Isento'}
                              </Typography>
                            </Grid>
                          )}
                        </Grid>
                        
                        <Divider sx={{ my: 2 }} />
                        
                        <Grid container spacing={2}>
                          {result.requirements && result.requirements.length > 0 && (
                            <Grid item xs={12} md={6}>
                              <Typography variant="body2" fontWeight="medium">
                                Requisitos:
                              </Typography>
                              <List dense>
                                {result.requirements.map((req, index) => (
                                  <ListItem key={index} disableGutters>
                                    <ListItemIcon sx={{ minWidth: 24 }}>
                                      <InfoIcon fontSize="small" />
                                    </ListItemIcon>
                                    <ListItemText primary={req} />
                                  </ListItem>
                                ))}
                              </List>
                            </Grid>
                          )}
                          
                          {result.documentation && result.documentation.length > 0 && (
                            <Grid item xs={12} md={6}>
                              <Typography variant="body2" fontWeight="medium">
                                Documentação Necessária:
                              </Typography>
                              <List dense>
                                {result.documentation.map((doc, index) => (
                                  <ListItem key={index} disableGutters>
                                    <ListItemIcon sx={{ minWidth: 24 }}>
                                      <InfoIcon fontSize="small" />
                                    </ListItemIcon>
                                    <ListItemText primary={doc} />
                                  </ListItem>
                                ))}
                              </List>
                            </Grid>
                          )}
                        </Grid>
                        
                        {result.restrictions && result.restrictions.length > 0 && (
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="body2" fontWeight="medium" color="error">
                              Restrições:
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                              {result.restrictions.map((restriction, index) => (
                                <Chip 
                                  key={index} 
                                  label={restriction} 
                                  size="small" 
                                  color="error" 
                                  variant="outlined" 
                                />
                              ))}
                            </Box>
                          </Box>
                        )}
                        
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 2 }}>
                          <Chip 
                            size="small" 
                            label={result.regulation_type === 'import' ? 'Importação' : 
                                  result.regulation_type === 'export' ? 'Exportação' : 
                                  result.regulation_type === 'tariff' ? 'Tarifas' :
                                  result.regulation_type} 
                          />
                          {result.effective_date && 
                            <Chip size="small" label={`Vigente desde: ${formatDate(result.effective_date)}`} />
                          }
                          {result.expiration_date && 
                            <Chip size="small" label={`Válido até: ${formatDate(result.expiration_date)}`} />
                          }
                        </Box>
                      </CardContent>
                      <CardActions>
                        {result.url && (
                          <Button 
                            size="small" 
                            href={result.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                          >
                            Ver Regulamento Original
                          </Button>
                        )}
                      </CardActions>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          ) : (
            results.length === 0 && !error && !loading && (
              <Box sx={{ textAlign: 'center', py: 6, px: 2 }}>
                <ShippingIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  Nenhuma regulamentação encontrada
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Tente modificar os critérios de busca para encontrar regulamentações alfandegárias.
                </Typography>
              </Box>
            )
          )}
        </>
      )}
    </Box>
  );
};

export default CustomsRegulationsSearch; 