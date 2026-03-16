'use client';

import { motion } from 'framer-motion';
import { Share2 } from 'lucide-react';
import { useState } from 'react';

interface SocialPublisherProps {
    jobId: string;
}

export default function SocialPublisher({ jobId }: SocialPublisherProps) {
    const [publishing, setPublishing] = useState<string | null>(null);

    const handlePublish = async (platform: 'tiktok' | 'instagram') => {
        setPublishing(platform);
        // In a real scenario, this opens an OAuth popup or redirects
        // After callback, it calls /api/v1/oauth/publish
        console.log(`Publishing job ${jobId} to ${platform}`);
        setTimeout(() => {
            window.location.href = `http://localhost:8000/api/v1/oauth/${platform}/login`;
            setPublishing(null);
        }, 1000);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-xl mx-auto backdrop-blur-xl bg-white/5 p-8 rounded-3xl border border-green-500/30 mt-8 shadow-[0_0_30px_rgba(34,197,94,0.1)] text-center relative overflow-hidden group"
        >
            <div className="absolute inset-0 bg-gradient-to-t from-green-500/10 to-transparent" />

            <div className="relative z-10 flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center mb-4">
                    <Share2 className="w-8 h-8 text-green-400" />
                </div>

                <h3 className="text-2xl font-bold text-white mb-2">Video Ready!</h3>
                <p className="text-zinc-400 mb-8 max-w-sm">
                    Your viral clip has been fully generated with automatic captions. Where do you want to publish it?
                </p>

                <div className="flex space-x-4 w-full justify-center">
                    <button
                        onClick={() => handlePublish('tiktok')}
                        disabled={publishing !== null}
                        className="flex-1 py-3 px-4 rounded-xl font-semibold transition-all bg-[#00f2fe]/10 hover:bg-[#00f2fe]/20 text-white border border-[#00f2fe]/30"
                    >
                        {publishing === 'tiktok' ? 'Publishing...' : 'TikTok'}
                    </button>

                    <button
                        onClick={() => handlePublish('instagram')}
                        disabled={publishing !== null}
                        className="flex-1 py-3 px-4 rounded-xl font-semibold transition-all bg-gradient-to-r from-purple-500/20 to-pink-500/20 hover:from-purple-500/30 hover:to-pink-500/30 text-white border border-pink-500/30"
                    >
                        {publishing === 'instagram' ? 'Publishing...' : 'Instagram Reels'}
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
