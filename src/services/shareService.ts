export const shareList = async (listId: string, email: string) => {
  // Implementation for sharing shopping list
  return fetch(`/api/share-list`, {
    method: 'POST',
    body: JSON.stringify({ listId, email }),
    headers: { 'Content-Type': 'application/json' }
  });
};
