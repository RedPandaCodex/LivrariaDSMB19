export interface Autor{
    id: number;
    autor: string;
    surname: string;
    birthdate?: string | null;
    nationality?: string | null;
    bio?: string | null;
}