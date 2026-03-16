'use client';

import { motion } from 'framer-motion';
import { CheckCircle2, Loader2 } from 'lucide-react';

interface ProgressTrackerProps {
    status: string;
    progress: number;
    message: string;
}

export default function ProgressTracker({ status, progress, message }: ProgressTrackerProps) {
    // Helper to determine step state based on hypothetical precise statuses,
    // but we can simplify by using the overall 'progress' number in a real scenario.

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-xl mx-auto backdrop-blur-xl bg-white/5 p-8 rounded-3xl border border-white/10 mt-8"
        >
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-white">Processing Video</h3>
                <span className="text-purple-400 font-mono">{progress}%</span>
            </div>

            {/* Progress Bar */}
            <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden mb-6">
                <motion.div
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.5 }}
                />
            </div>

            <div className="flex items-center space-x-4 text-zinc-300">
                {status === 'completed' ? (
                    <CheckCircle2 className="w-5 h-5 text-green-400" />
                ) : (
                    <Loader2 className="w-5 h-5 animate-spin text-purple-400" />
                )}
                <p className="text-sm">{message || 'Initializing...'}</p>
            </div>
        </motion.div>
    );
}
