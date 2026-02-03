import React from 'react';

const AlbumDesignerLayout = () => {
  return (
    <div className="flex h-full w-full gap-4 p-4">
      {/* Left Panel: Inputs */}
      <div className="w-1/3 flex flex-col gap-4 bg-slate-800/50 p-4 rounded-xl border border-white/10">
        <h2 className="text-xl font-bold text-indigo-400">Design Studio</h2>
        <div className="flex-1">
             {/* GenerateForm */}
             <GenerateForm />
        </div>
      </div>

      {/* Right Panel: Output/Preview */}
      <div className="flex-1 flex flex-col gap-4 bg-slate-800/50 p-4 rounded-xl border border-white/10">
        <h2 className="text-xl font-bold text-purple-400">Blueprint Preview</h2>
        <div className="flex-1">
            {/* Results will go here */}
            <div className="p-4 bg-slate-900/50 rounded-lg border border-dashed border-slate-700 h-full flex items-center justify-center text-slate-500">
                Results Placeholder
            </div>
        </div>
      </div>
    </div>
  );
};

export default AlbumDesignerLayout;
