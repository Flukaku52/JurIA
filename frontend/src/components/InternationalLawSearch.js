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
  Paper
} from '@mui/material';
import axios from 'axios';
import { Search as SearchIcon, Public as PublicIcon } from '@mui/icons-material';

const InternationalLawSearch = () => {
  const [searchParams, setSearchParams] = useState({
    query: '',
    jurisdiction: '',
    category: ''
  });
  
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('general'); // 'general', 'singapore', 'customs'
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleSearch = async () => {
    if (!searchParams.query && activeTab === 'general') {
      setError('Por favor, insira um termo de busca');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      let endpoint = '/api/international-law/search';
      let params = { ...searchParams };
      
      if (activeTab === 'singapore') {
        endpoint = '/api/international-law/singapore';
        params = { category: searchParams.category };
      } else if (activeTab === 'customs') {
        endpoint = '/api/international-law/customs';
        // Adaptar parâmetros se necessário
      }
      
      const response = await axios.get(endpoint, { params });
      setResults(response.data);
    } catch (err) {
      console.error('Erro ao buscar leis internacionais:', err);
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
        <PublicIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        Consulta de Direito Internacional
      </Typography>
      
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ mb: 2 }}>
          <Button 
            variant={activeTab === 'general' ? 'contained' : 'outlined'} 
            onClick={() => setActiveTab('general')}
            sx={{ mr: 1 }}
          >
            Direito Internacional
          </Button>
          <Button 
            variant={activeTab === 'singapore' ? 'contained' : 'outlined'} 
            onClick={() => setActiveTab('singapore')}
            sx={{ mr: 1 }}
          >
            Legislação de Singapura
          </Button>
          <Button 
            variant={activeTab === 'customs' ? 'contained' : 'outlined'} 
            onClick={() => setActiveTab('customs')}
          >
            Políticas Alfandegárias
          </Button>
        </Box>
        
        <Grid container spacing={2}>
          {activeTab === 'general' && (
            <>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Termo de Busca"
                  name="query"
                  value={searchParams.query}
                  onChange={handleInputChange}
                  placeholder="Ex: tratados internacionais, comércio"
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} md={3}>
                <FormControl fullWidth variant="outlined">
                  <InputLabel>Jurisdição</InputLabel>
                  <Select
                    name="jurisdiction"
                    value={searchParams.jurisdiction}
                    onChange={handleInputChange}
                    label="Jurisdição"
                  >
                    <MenuItem value="">Todas</MenuItem>
                    <MenuItem value="global">Global</MenuItem>
                    <MenuItem value="singapore">Singapura</MenuItem>
                    <MenuItem value="eu">União Europeia</MenuItem>
                    <MenuItem value="usa">Estados Unidos</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </>
          )}
          
          <Grid item xs={12} md={activeTab === 'general' ? 3 : 6}>
            <FormControl fullWidth variant="outlined">
              <InputLabel>Categoria</InputLabel>
              <Select
                name="category"
                value={searchParams.category}
                onChange={handleInputChange}
                label="Categoria"
              >
                <MenuItem value="">Todas</MenuItem>
                {activeTab === 'general' && (
                  <>
                    <MenuItem value="treaties">Tratados</MenuItem>
                    <MenuItem value="trade">Comércio</MenuItem>
                    <MenuItem value="customs">Alfândega</MenuItem>
                  </>
                )}
                {activeTab === 'singapore' && (
                  <>
                    <MenuItem value="business">Empresarial</MenuItem>
                    <MenuItem value="tax">Tributário</MenuItem>
                    <MenuItem value="customs">Alfândega</MenuItem>
                    <MenuItem value="investment">Investimento</MenuItem>
                  </>
                )}
                {activeTab === 'customs' && (
                  <>
                    <MenuItem value="import">Importação</MenuItem>
                    <MenuItem value="export">Exportação</MenuItem>
                    <MenuItem value="tariff">Tarifas</MenuItem>
                  </>
                )}
              </Select>
            </FormControl>
          </Grid>
          
          {activeTab === 'customs' && (
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Código do Produto (HS Code)"
                name="productCode"
                placeholder="Ex: 8471.30"
                variant="outlined"
              />
            </Grid>
          )}
          
          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleSearch}
              startIcon={<SearchIcon />}
              disabled={loading}
            >
              {loading ? 'Buscando...' : 'Buscar'}
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
                          <Typography variant="h6">{result.title}</Typography>
                          <Chip 
                            label={result.jurisdiction === 'singapore' ? 'Singapura' : 
                                   result.jurisdiction === 'global' ? 'Global' : 
                                   result.jurisdiction}
                            color={result.jurisdiction === 'singapore' ? 'primary' : 'default'}
                            size="small"
                          />
                        </Box>
                        <Divider sx={{ mb: 2 }} />
                        <Typography variant="body2" color="text.secondary" paragraph>
                          {result.content}
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 2 }}>
                          <Chip size="small" label={`Categoria: ${result.category}`} />
                          <Chip size="small" label={`Fonte: ${result.source}`} />
                          {result.publication_date && 
                            <Chip size="small" label={`Publicado: ${formatDate(result.publication_date)}`} />
                          }
                          {result.last_updated && 
                            <Chip size="small" label={`Atualizado: ${formatDate(result.last_updated)}`} />
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
                            Ver Documento Original
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
              <Typography variant="body1" color="text.secondary" align="center">
                Nenhum resultado encontrado. Tente modificar os termos da busca.
              </Typography>
            )
          )}
        </>
      )}
    </Box>
  );
};

export default InternationalLawSearch; 