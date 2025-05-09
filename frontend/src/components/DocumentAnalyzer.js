import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Grid,
  Divider,
  CircularProgress,
  Paper,
  TextField,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Collapse
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Description as DocumentIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import axios from 'axios';

const DocumentAnalyzer = () => {
  const [selectedDocumentType, setSelectedDocumentType] = useState('');
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [expanded, setExpanded] = useState({
    recommendations: true,
    regulations: false
  });

  const documentTypes = [
    { value: 'invoice', label: 'Fatura Comercial (Invoice)' },
    { value: 'bl', label: 'Conhecimento de Embarque (BL)' },
    { value: 'packing_list', label: 'Lista de Embalagem (Packing List)' },
    { value: 'certificate_of_origin', label: 'Certificado de Origem' }
  ];

  const handleDocumentTypeChange = (event) => {
    setSelectedDocumentType(event.target.value);
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleExpandToggle = (section) => {
    setExpanded(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handleSubmit = async () => {
    if (!selectedDocumentType || !file) {
      setError('Por favor, selecione um tipo de documento e faça upload de um arquivo.');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        `/api/international-law/upload-document?document_type=${selectedDocumentType}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      setAnalysisResult(response.data);
    } catch (err) {
      console.error('Erro ao analisar documento:', err);
      setError(err.response?.data?.detail || 'Erro ao processar o documento. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'compliant':
        return <CheckIcon style={{ color: 'green' }} />;
      case 'warning':
        return <WarningIcon style={{ color: 'orange' }} />;
      case 'non_compliant':
        return <ErrorIcon style={{ color: 'red' }} />;
      default:
        return <InfoIcon color="primary" />;
    }
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        <DocumentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        Análise de Documentos Alfandegários
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth variant="outlined">
              <InputLabel>Tipo de Documento</InputLabel>
              <Select
                value={selectedDocumentType}
                onChange={handleDocumentTypeChange}
                label="Tipo de Documento"
              >
                <MenuItem value="">
                  <em>Selecione um tipo de documento</em>
                </MenuItem>
                {documentTypes.map(type => (
                  <MenuItem key={type.value} value={type.value}>
                    {type.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Button
                variant="contained"
                component="label"
                startIcon={<UploadIcon />}
                sx={{ mr: 2 }}
              >
                Selecionar Arquivo
                <input
                  type="file"
                  hidden
                  onChange={handleFileChange}
                  accept=".pdf,.docx,.xml,.json"
                />
              </Button>
              <Typography variant="body2" color="text.secondary">
                {fileName || 'Nenhum arquivo selecionado'}
              </Typography>
            </Box>
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              Formatos suportados: PDF, DOCX, XML, JSON
            </Typography>
          </Grid>
          
          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleSubmit}
              disabled={loading || !selectedDocumentType || !file}
              startIcon={loading ? <CircularProgress size={20} /> : <DocumentIcon />}
            >
              {loading ? 'Analisando...' : 'Analisar Documento'}
            </Button>
          </Grid>
        </Grid>
        
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        analysisResult && (
          <Card variant="outlined" sx={{ mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                {getStatusIcon(analysisResult.compliance_status)}
                <Typography variant="h6" sx={{ ml: 1 }}>
                  Resultado da Análise: {' '}
                  {analysisResult.compliance_status === 'compliant' && 'Conforme'}
                  {analysisResult.compliance_status === 'warning' && 'Atenção Necessária'}
                  {analysisResult.compliance_status === 'non_compliant' && 'Não Conforme'}
                </Typography>
              </Box>
              
              <Divider sx={{ mb: 2 }} />
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" gutterBottom fontWeight="bold">
                    Informações do Documento
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2">
                      <strong>Tipo de Documento:</strong> {
                        documentTypes.find(t => t.value === analysisResult.document_type)?.label || 
                        analysisResult.document_type
                      }
                    </Typography>
                    {analysisResult.file_info && (
                      <>
                        <Typography variant="body2">
                          <strong>Nome do Arquivo:</strong> {analysisResult.file_info.filename}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Tipo de Conteúdo:</strong> {analysisResult.file_info.content_type}
                        </Typography>
                      </>
                    )}
                    <Typography variant="body2">
                      <strong>Data da Análise:</strong> {
                        new Date(analysisResult.analysis_timestamp).toLocaleString('pt-BR')
                      }
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" gutterBottom fontWeight="bold">
                    Status de Conformidade
                  </Typography>
                  
                  {analysisResult.missing_fields.length > 0 && (
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="body2" color="error" fontWeight="medium">
                        Campos Obrigatórios Ausentes:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                        {analysisResult.missing_fields.map((field, index) => (
                          <Chip 
                            key={index} 
                            label={field} 
                            size="small" 
                            color="error" 
                            variant="outlined" 
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                  
                  {analysisResult.missing_info.length > 0 && (
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="body2" color="warning.main" fontWeight="medium">
                        Informações Adicionais Necessárias:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                        {analysisResult.missing_info.map((info, index) => (
                          <Chip 
                            key={index} 
                            label={info} 
                            size="small" 
                            color="warning" 
                            variant="outlined" 
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                  
                  {analysisResult.compliance_issues.length > 0 && (
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="body2" color="error" fontWeight="medium">
                        Problemas de Conformidade:
                      </Typography>
                      <List dense>
                        {analysisResult.compliance_issues.map((issue, index) => (
                          <ListItem key={index} disableGutters>
                            <ListItemIcon sx={{ minWidth: 24 }}>
                              <ErrorIcon fontSize="small" color="error" />
                            </ListItemIcon>
                            <ListItemText primary={issue} />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}
                  
                  {analysisResult.missing_fields.length === 0 && 
                   analysisResult.missing_info.length === 0 &&
                   analysisResult.compliance_issues.length === 0 && (
                    <Alert severity="success">
                      O documento está em conformidade com os requisitos.
                    </Alert>
                  )}
                </Grid>
              </Grid>
              
              <Divider sx={{ my: 2 }} />
              
              <Box>
                <Box 
                  sx={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    cursor: 'pointer'
                  }}
                  onClick={() => handleExpandToggle('recommendations')}
                >
                  <Typography variant="subtitle1" fontWeight="bold">
                    Recomendações
                  </Typography>
                  <IconButton size="small">
                    {expanded.recommendations ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  </IconButton>
                </Box>
                
                <Collapse in={expanded.recommendations}>
                  {analysisResult.recommendations.length > 0 ? (
                    <List dense>
                      {analysisResult.recommendations.map((recommendation, index) => (
                        <ListItem key={index} disableGutters>
                          <ListItemIcon sx={{ minWidth: 24 }}>
                            <InfoIcon fontSize="small" color="primary" />
                          </ListItemIcon>
                          <ListItemText primary={recommendation} />
                        </ListItem>
                      ))}
                    </List>
                  ) : (
                    <Typography variant="body2" color="text.secondary" sx={{ pl: 2, pt: 1 }}>
                      Nenhuma recomendação necessária.
                    </Typography>
                  )}
                </Collapse>
              </Box>
              
              {analysisResult.related_regulations && analysisResult.related_regulations.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Box 
                    sx={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center',
                      cursor: 'pointer'
                    }}
                    onClick={() => handleExpandToggle('regulations')}
                  >
                    <Typography variant="subtitle1" fontWeight="bold">
                      Regulamentos Relacionados
                    </Typography>
                    <IconButton size="small">
                      {expanded.regulations ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                    </IconButton>
                  </Box>
                  
                  <Collapse in={expanded.regulations}>
                    <Grid container spacing={2} sx={{ mt: 0.5 }}>
                      {analysisResult.related_regulations.map((regulation) => (
                        <Grid item xs={12} key={regulation.id}>
                          <Card variant="outlined">
                            <CardContent sx={{ pb: 1 }}>
                              <Typography variant="h6">{regulation.title}</Typography>
                              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1, mb: 1 }}>
                                <Chip 
                                  label={regulation.country === 'singapore' ? 'Singapura' : regulation.country} 
                                  size="small" 
                                  color="primary" 
                                  variant="outlined" 
                                />
                                <Chip 
                                  label={regulation.regulation_type === 'import' ? 'Importação' : 
                                         regulation.regulation_type === 'export' ? 'Exportação' : 
                                         regulation.regulation_type === 'tariff' ? 'Tarifas' : 
                                         regulation.regulation_type} 
                                  size="small" 
                                  variant="outlined" 
                                />
                              </Box>
                              <Typography variant="body2" color="text.secondary">
                                {regulation.content}
                              </Typography>
                              
                              {regulation.requirements && regulation.requirements.length > 0 && (
                                <Box sx={{ mt: 1 }}>
                                  <Typography variant="body2" fontWeight="medium">
                                    Requisitos:
                                  </Typography>
                                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                                    {regulation.requirements.map((req, index) => (
                                      <Chip key={index} label={req} size="small" />
                                    ))}
                                  </Box>
                                </Box>
                              )}
                            </CardContent>
                            {regulation.url && (
                              <Box sx={{ px: 2, pb: 1 }}>
                                <Button 
                                  size="small" 
                                  href={regulation.url} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                >
                                  Ver Documento Original
                                </Button>
                              </Box>
                            )}
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  </Collapse>
                </Box>
              )}
            </CardContent>
          </Card>
        )
      )}
      
      {!loading && !analysisResult && (
        <Box sx={{ textAlign: 'center', py: 6, px: 2 }}>
          <DocumentIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Faça upload de um documento para análise
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Selecione um tipo de documento e faça upload do arquivo para verificar sua conformidade com regulamentações alfandegárias.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default DocumentAnalyzer; 