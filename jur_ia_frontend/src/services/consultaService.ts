import api from './api';
import type { ConsultaCreate, ConsultaHistorico, ConsultaResponse } from '../types/consulta';

export const consultaService = {
  async criarConsulta(consulta: ConsultaCreate): Promise<ConsultaResponse> {
    const response = await api.post<ConsultaResponse>('/consulta-juris', consulta);
    return response.data;
  },

  async listarConsultas(
    skip: number = 0,
    limit: number = 10,
    status?: string
  ): Promise<ConsultaHistorico[]> {
    const params = { skip, limit, status };
    const response = await api.get<ConsultaHistorico[]>('/consulta-juris', { params });
    return response.data;
  },

  async obterConsulta(id: number): Promise<ConsultaResponse> {
    const response = await api.get<ConsultaResponse>(`/consulta-juris/${id}`);
    return response.data;
  },
}; 