'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Youtube, ArrowRight, Loader2 } from 'lucide-react';

interface VideoLinkInputProps {
    onSubmit: (url: string) => void;
    isLoading: boolean;
}

export default function VideoLinkInput({ onSubmit, isLoading }: VideoLinkInputProps) {
    const [url, setUrl] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
            setError('Please enter a valid YouTube URL');
            return;
        }
        setError('');
        onSubmit(url);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="w-full max-w-xl mx-auto backdrop-blur-xl bg-white/5 p-8 rounded-3xl border border-white/10 shadow-[0_0_40px_rgba(255,255,255,0.1)] relative overflow-hidden group"
        >
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

            <div className="relative z-10">
                <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">
                    Create Viral Shorts
                </h2>
                <p className="text-zinc-400 mb-8 text-sm">
                    Paste a YouTube link below. We'll download, add captions, and format it for TikTok & Instagram.
                </p>

                <form onSubmit={handleSubmit} className="relative">
                    <div className="relative flex items-center">
                        <Youtube className="absolute left-4 w-5 h-5 text-zinc-400" />
                        <input
                            type="text"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            placeholder="https://www.youtube.com/watch?v=..."
                            disabled={isLoading}
                            className="w-full bg-black/40 border border-white/10 text-white rounded-2xl py-4 pl-12 pr-16 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all placeholder:text-zinc-600 disabled:opacity-50"
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !url}
                            className="absolute right-2 p-2 bg-white text-black rounded-xl hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:hover:scale-100 flex items-center justify-center"
                        >
                            {isLoading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <ArrowRight className="w-5 h-5" />
                            )}
                        </button>
                    </div>

                    <AnimatePresence>
                        {error && (
                            <motion.p
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                className="text-red-400 text-sm mt-3 ml-2"
                            >
                                {error}
                            </motion.p>
                        )}
                    </AnimatePresence>
                </form>
            </div>
        </motion.div>
    );
}
