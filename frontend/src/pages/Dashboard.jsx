import { useState, useEffect } from 'react'
import { getAlbums, getQueue } from '../services/api'

export default function Dashboard() {
    const [albums, setAlbums] = useState([])
    const [queue, setQueue] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadData()
    }, [])

    const loadData = async () => {
        try {
            const [albumsRes, queueRes] = await Promise.all([
                getAlbums(),
                getQueue()
            ])
            setAlbums(albumsRes.data)
            setQueue(queueRes.data)
        } catch (error) {
            console.error('Failed to load data:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="text-xl text-gray-400">Loading...</div>
            </div>
        )
    }

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold text-white mb-6">Dashboard</h2>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 backdrop-blur-lg rounded-xl p-6 border border-purple-500/30">
                        <div className="text-4xl mb-2">📀</div>
                        <div className="text-3xl font-bold text-white">{albums.length}</div>
                        <div className="text-gray-400">Total Albums</div>
                    </div>

                    <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 backdrop-blur-lg rounded-xl p-6 border border-blue-500/30">
                        <div className="text-4xl mb-2">🎵</div>
                        <div className="text-3xl font-bold text-white">{queue.length}</div>
                        <div className="text-gray-400">Pending Tracks</div>
                    </div>

                    <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 backdrop-blur-lg rounded-xl p-6 border border-green-500/30">
                        <div className="text-4xl mb-2">✨</div>
                        <div className="text-3xl font-bold text-white">
                            {albums.reduce((sum, a) => sum + a.tracks.length, 0)}
                        </div>
                        <div className="text-gray-400">Total Tracks</div>
                    </div>
                </div>

                {/* Recent Albums */}
                <div className="bg-black/30 backdrop-blur-lg rounded-xl p-6 border border-purple-500/20">
                    <h3 className="text-xl font-semibold text-white mb-4">Recent Albums</h3>

                    {albums.length === 0 ? (
                        <div className="text-center py-8 text-gray-400">
                            No albums yet. Design your first album!
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {albums.slice(0, 5).map(album => (
                                <div key={album.id} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
                                    <div>
                                        <div className="font-semibold text-white">{album.title}</div>
                                        <div className="text-sm text-gray-400">{album.archetype} • {album.tracks.length} tracks</div>
                                    </div>
                                    <div className="text-sm text-gray-500">
                                        {new Date(album.created_at).toLocaleDateString()}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
