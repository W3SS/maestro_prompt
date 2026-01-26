import { useState } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import AlbumDesigner from './pages/AlbumDesigner'
import QueueViewer from './pages/QueueViewer'

function App() {
    return (
        <BrowserRouter>
            <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
                {/* Navigation */}
                <nav className="bg-black/30 backdrop-blur-lg border-b border-purple-500/20">
                    <div className="container mx-auto px-6 py-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-2">
                                <span className="text-3xl">🎹</span>
                                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
                                    Maestro AI
                                </h1>
                            </div>

                            <div className="flex space-x-6">
                                <Link to="/" className="text-gray-300 hover:text-white transition">
                                    Dashboard
                                </Link>
                                <Link to="/design" className="text-gray-300 hover:text-white transition">
                                    Design Album
                                </Link>
                                <Link to="/queue" className="text-gray-300 hover:text-white transition">
                                    Queue
                                </Link>
                            </div>
                        </div>
                    </div>
                </nav>

                {/* Routes */}
                <div className="container mx-auto px-6 py-8">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/design" element={<AlbumDesigner />} />
                        <Route path="/queue" element={<QueueViewer />} />
                    </Routes>
                </div>
            </div>
        </BrowserRouter>
    )
}

export default App
