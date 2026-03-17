'use client';

import { motion } from 'framer-motion';
import { Download, Share2 } from 'lucide-react';

interface VideoResultPlayerProps {
    videoUrl: string;
}

export default function VideoResultPlayer({ videoUrl }: VideoResultPlayerProps) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="w-full max-w-sm mx-auto backdrop-blur-xl bg-white/5 p-6 rounded-3xl border border-white/10 shadow-[0_0_40px_rgba(255,255,255,0.1)] relative overflow-hidden group mt-6"
        >
            <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/10 via-transparent to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            
            <div className="relative z-10 flex flex-col items-center">
                <h3 className="text-xl font-bold text-white mb-4 tracking-tight">
                    Your Viral Short is Ready ✨
                </h3>
                
                {/* 9:16 Video Player Container */}
                <div className="w-full aspect-[9/16] bg-black/50 rounded-2xl overflow-hidden border border-white/10 shadow-2xl relative">
                    <video 
                        src={videoUrl} 
                        controls 
                        autoPlay 
                        loop 
                        className="w-full h-full object-cover"
                        crossOrigin="anonymous"
                    >
                        Your browser does not support the video tag.
                    </video>
                </div>
                
                {/* Action Buttons */}
                <div className="flex w-full space-x-4 mt-6">
                    <a 
                        href={videoUrl}
                        download="autocut-viral-short.mp4"
                        target="_blank"
                        rel="noreferrer"
                        className="flex-1 bg-white/10 hover:bg-white/20 text-white font-medium py-3 px-4 rounded-xl flex items-center justify-center transition-all hover:scale-[1.02] active:scale-95 border border-white/5"
                    >
                        <Download className="w-4 h-4 mr-2" />
                        Download
                    </a>
                    
                    <button 
                        onClick={() => {
                            if (navigator.share) {
                                navigator.share({
                                    title: 'My Viral Short',
                                    url: videoUrl
                                });
                            } else {
                                navigator.clipboard.writeText(videoUrl);
                                alert("Link copied to clipboard!");
                            }
                        }}
                        className="flex-1 bg-gradient-to-r from-purple-500 hover:from-purple-400 to-pink-500 hover:to-pink-400 text-white font-medium py-3 px-4 rounded-xl flex items-center justify-center transition-all hover:scale-[1.02] active:scale-95 shadow-lg shadow-purple-500/25"
                    >
                        <Share2 className="w-4 h-4 mr-2" />
                        Share
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
