import React, { useCallback, useMemo } from 'react';
import { 
  Container, 
  Typography, 
  TextField, 
  Button, 
  Paper, 
  Box, 
  CircularProgress,
  Alert
} from '@mui/material';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useConsultaStore } from '../store/consultaStore';
import type { ConsultaCreate } from '../types/consulta';

// Interface específica para o formulário
interface FormValues {
  pergunta: string;
  contexto: string;
}

// Schema de validação do formulário
const schema = yup.object().shape({
  pergunta: yup.string().required('A pergunta é obrigatória').min(5, 'A pergunta deve ter pelo menos 5 caracteres'),
  contexto: yup.string(),
});

// Componente para renderizar a resposta da consulta
const RespostaConsulta = React.memo(({ resposta, dataCriacao }: { resposta: string; dataCriacao: string }) => {
  const dataFormatada = useMemo(() => {
    if (!dataCriacao) return '';
    const data = new Date(dataCriacao);
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    }).format(data);
  }, [dataCriacao]);

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 4, bgcolor: '#f9f9f9' }}>
      <Typography variant="subtitle2" color="textSecondary" gutterBottom>
        Consulta realizada em: {dataFormatada}
      </Typography>
      <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
        {resposta}
      </Typography>
    </Paper>
  );
});

RespostaConsulta.displayName = 'RespostaConsulta';

const ConsultaPage: React.FC = () => {
  const { consultaAtual, loading, error, criarConsulta, limparErro } = useConsultaStore();
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm<FormValues>({
    resolver: yupResolver(schema),
    defaultValues: {
      pergunta: '',
      contexto: '',
    }
  });

  // Callback para enviar o formulário
  const onSubmit = useCallback((data: FormValues) => {
    const consultaData: ConsultaCreate = {
      pergunta: data.pergunta,
      ...(data.contexto ? { contexto: data.contexto } : {})
    };
    
    criarConsulta(consultaData.pergunta)
      .then(() => reset())
      .catch((error) => console.error('Erro ao criar consulta:', error));
  }, [criarConsulta, reset]);

  // Renderização memoizada do formulário
  const formularioConsulta = useMemo(() => (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 3 }}>
      <TextField
        fullWidth
        multiline
        rows={4}
        label="Sua pergunta jurídica"
        placeholder="Digite sua pergunta sobre legislação, jurisprudência ou dúvida jurídica..."
        variant="outlined"
        margin="normal"
        {...register('pergunta')}
        error={!!errors.pergunta}
        helperText={errors.pergunta?.message}
      />
      
      <TextField
        fullWidth
        multiline
        rows={2}
        label="Contexto adicional (opcional)"
        placeholder="Forneça mais detalhes ou contexto para sua pergunta..."
        variant="outlined"
        margin="normal"
        {...register('contexto')}
        error={!!errors.contexto}
        helperText={errors.contexto?.message}
      />
      
      <Button 
        type="submit" 
        variant="contained" 
        color="primary"
        size="large"
        fullWidth
        sx={{ mt: 2 }}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : 'Enviar Consulta'}
      </Button>
    </Box>
  ), [handleSubmit, onSubmit, register, errors, loading]);

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Consulta Jurídica
        </Typography>
        
        <Typography variant="body1" align="center" sx={{ mb: 4 }}>
          Faça sua pergunta e receba uma resposta baseada em conhecimento jurídico especializado.
        </Typography>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={limparErro}>
            {error}
          </Alert>
        )}
        
        {formularioConsulta}
        
        {consultaAtual && (
          <RespostaConsulta 
            resposta={consultaAtual.resposta}
            dataCriacao={consultaAtual.data_criacao}
          />
        )}
      </Box>
    </Container>
  );
};

export default React.memo(ConsultaPage); 