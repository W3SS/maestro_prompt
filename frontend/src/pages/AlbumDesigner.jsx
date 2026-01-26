import { useState, useEffect } from 'react'
import { getArchetypes, designAlbum } from '../services/api'
import { useNavigate } from 'react-router-dom'

export default function AlbumDesigner() {
    const [archetypes, setArchetypes] = useState([])
    const [selectedArchetype, setSelectedArchetype] = useState('')
    const [title, setTitle] = useState('')
    const [numTracks, setNumTracks] = useState(8)
    const [loading, setLoading] = useState(false)
    const [searchTerm, setSearchTerm] = useState('')
    const navigate = useNavigate()

    useEffect(() => {
        loadArchetypes()
    }, [])

    const loadArchetypes = async () => {
        try {
            const res = await getArchetypes()
            setArchetypes(res.data)
        } catch (error) {
            console.error('Failed to load archetypes:', error)
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)

        try {
            await designAlbum({
                archetype: selectedArchetype,
                title: title || undefined,
                num_tracks: numTracks
            })

            alert('Album designed successfully!')
            navigate('/queue')
        } catch (error) {
            console.error('Failed to design album:', error)
            alert('Failed to design album. Check console for details.')
        } finally {
            setLoading(false)
        }
    }

    const filteredArchetypes = archetypes.filter(a =>
        a.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        a.directorial_tone?.toLowerCase().includes(searchTerm.toLowerCase())
    )

    return (
        <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-white mb-6">Design New Album</h2>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Archetype Selection */}
                <div className="bg-black/30 backdrop-blur-lg rounded-xl p-6 border border-purple-500/20">
                    <label className="block text-white font-semibold mb-3">
                        Select Archetype *
                    </label>

                    <input
                        type="text"
                        placeholder="Search archetypes..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full px-4 py-2 bg-white/10 border border-purple-500/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 mb-4"
                    />

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-96 overflow-y-auto">
                        {filteredArchetypes.map(archetype => (
                            <div
                                key={archetype.id}
                                onClick={() => setSelectedArchetype(archetype.id)}
                                className={`p-4 rounded-lg cursor-pointer transition ${selectedArchetype === archetype.id
                                        ? 'bg-purple-500/30 border-2 border-purple-500'
                                        : 'bg-white/5 border border-white/10 hover:bg-white/10'
                                    }`}
                            >
                                <div className="font-semibold text-white mb-1">{archetype.id}</div>
                                <div className="text-sm text-gray-400 line-clamp-2">
                                    {archetype.directorial_tone}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Album Details */}
                <div className="bg-black/30 backdrop-blur-lg rounded-xl p-6 border border-purple-500/20">
                    <label className="block text-white font-semibold mb-3">
                        Album Title (optional)
                    </label>
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        placeholder="Leave empty to auto-generate"
                        className="w-full px-4 py-2 bg-white/10 border border-purple-500/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
                    />
                </div>

                <div className="bg-black/30 backdrop-blur-lg rounded-xl p-6 border border-purple-500/20">
                    <label className="block text-white font-semibold mb-3">
                        Number of Tracks: {numTracks}
                    </label>
                    <input
                        type="range"
                        min="4"
                        max="12"
                        value={numTracks}
                        onChange={(e) => setNumTracks(parseInt(e.target.value))}
                        className="w-full"
                    />
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={!selectedArchetype || loading}
                    className="w-full py-4 bg-gradient-to-r from-purple-500 to-pink-600 text-white font-bold rounded-lg hover:from-purple-600 hover:to-pink-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {loading ? 'Designing Album...' : '🎨 Design Album'}
                </button>
            </form>
        </div>
    )
}
