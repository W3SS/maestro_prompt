import { useState, useEffect } from 'react'
import { getQueue, generateSongs } from '../services/api'

export default function QueueViewer() {
    const [queue, setQueue] = useState([])
    const [loading, setLoading] = useState(true)
    const [generating, setGenerating] = useState(false)

    useEffect(() => {
        loadQueue()
    }, [])

    const loadQueue = async () => {
        try {
            const res = await getQueue()
            setQueue(res.data)
        } catch (error) {
            console.error('Failed to load queue:', error)
        } finally {
            setLoading(false)
        }
    }

    const handleGenerate = async () => {
        if (!confirm('Start generating all pending tracks?')) return

        setGenerating(true)
        try {
            await generateSongs()
            alert('Generation started! Tracks will be processed in the background.')
            loadQueue()
        } catch (error) {
            console.error('Failed to start generation:', error)
            alert('Failed to start generation. Check console for details.')
        } finally {
            setGenerating(false)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="text-xl text-gray-400">Loading queue...</div>
            </div>
        )
    }

    return (
        <div>
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-3xl font-bold text-white">Generation Queue</h2>

                {queue.length > 0 && (
                    <button
                        onClick={handleGenerate}
                        disabled={generating}
                        className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold rounded-lg hover:from-green-600 hover:to-emerald-700 transition disabled:opacity-50"
                    >
                        {generating ? 'Starting...' : `🚀 Generate ${queue.length} Tracks`}
                    </button>
                )}
            </div>

            {queue.length === 0 ? (
                <div className="bg-black/30 backdrop-blur-lg rounded-xl p-12 border border-purple-500/20 text-center">
                    <div className="text-6xl mb-4">✅</div>
                    <div className="text-xl text-white mb-2">Queue is empty!</div>
                    <div className="text-gray-400">All tracks have been processed or no albums designed yet.</div>
                </div>
            ) : (
                <div className="bg-black/30 backdrop-blur-lg rounded-xl p-6 border border-purple-500/20">
                    <div className="space-y-3">
                        {queue.map((track, index) => (
                            <div key={track.id} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
                                <div className="flex items-center space-x-4">
                                    <div className="text-2xl font-bold text-purple-400">#{index + 1}</div>
                                    <div>
                                        <div className="font-semibold text-white">{track.title}</div>
                                        <div className="text-sm text-gray-400">
                                            {track.genre} • {track.mood}
                                        </div>
                                    </div>
                                </div>

                                <div className="text-right">
                                    <div className="text-sm text-gray-500">Album: {track.album_id.substring(0, 8)}</div>
                                    <div className="text-xs text-gray-600">{track.status}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
