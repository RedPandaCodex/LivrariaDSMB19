export interface Autor {
  id: number;
  nome: string;
  sobrenome: string;
  data_nascimento?: string | null;
  nacionalidade?: string | null;
  biografia?: string | null;
}
