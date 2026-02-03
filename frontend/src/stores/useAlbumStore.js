import { create } from 'zustand';

const useAlbumStore = create((set) => ({
  // State
  generatedAlbum: null,
  isGenerating: false,
  error: null,
  
  // Actions
  setGeneratedAlbum: (album) => set({ generatedAlbum: album }),
  setIsGenerating: (isGenerating) => set({ isGenerating }),
  setError: (error) => set({ error }),
  
  // Reset
  reset: () => set({ generatedAlbum: null, isGenerating: false, error: null }),
}));

export default useAlbumStore;
