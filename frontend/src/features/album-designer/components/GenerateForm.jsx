import React from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import useAlbumStore from '../../../stores/useAlbumStore';
import { Sparkles, Music, Disc } from 'lucide-react';

const schema = z.object({
  artist: z.string().min(1, 'Artist name is required'),
  genre: z.string().min(1, 'Genre is required'),
  theme: z.string().optional(),
  trackCount: z.number().min(1).max(20).default(5),
});

const GenerateForm = () => {
  const { isGenerating, setIsGenerating } = useAlbumStore();
  
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
    defaultValues: {
      trackCount: 5
    }
  });

  const onSubmit = async (data) => {
    setIsGenerating(true);
    console.log('Generating with:', data);
    // TODO: Call API
    setTimeout(() => setIsGenerating(false), 2000); // Mock
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 text-white">
      {/* Artist */}
      <div className="flex flex-col gap-1">
        <label className="text-sm text-slate-400 flex items-center gap-2">
            <Music size={14} /> Artist / Band
        </label>
        <input 
          {...register('artist')}
          className="bg-slate-900 border border-slate-700 rounded-md p-2 focus:border-indigo-500 outline-none" 
          placeholder="e.g. Cyberpunk Orchestra"
        />
        {errors.artist && <span className="text-xs text-red-400">{errors.artist.message}</span>}
      </div>

      {/* Genre */}
      <div className="flex flex-col gap-1">
        <label className="text-sm text-slate-400 flex items-center gap-2">
            <Disc size={14} /> Genre
        </label>
        <input 
          {...register('genre')}
          className="bg-slate-900 border border-slate-700 rounded-md p-2 focus:border-indigo-500 outline-none" 
          placeholder="e.g. Industrial Metal"
        />
        {errors.genre && <span className="text-xs text-red-400">{errors.genre.message}</span>}
      </div>
      
       {/* Theme */}
      <div className="flex flex-col gap-1">
        <label className="text-sm text-slate-400">Theme (Optional)</label>
        <textarea 
          {...register('theme')}
          rows={3}
          className="bg-slate-900 border border-slate-700 rounded-md p-2 focus:border-indigo-500 outline-none resize-none" 
          placeholder="Describe the vibe..."
        />
      </div>

      <button 
        type="submit" 
        disabled={isGenerating}
        className="mt-4 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white p-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors"
      >
        {isGenerating ? (
            <span className="animate-pulse">Analyzing DNA...</span> 
        ) : (
            <>
                <Sparkles size={18} /> Generate Album
            </>
        )}
      </button>
    </form>
  );
};

export default GenerateForm;
