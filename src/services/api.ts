import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL
});

export const getShoppingLists = () => api.get('/shopping-lists');
export const createShoppingList = (data: any) => api.post('/shopping-lists', data);
export const updateShoppingList = (id: string, data: any) => api.put(`/shopping-lists/${id}`, data);
