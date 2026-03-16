'use client';

import Spline from '@splinetool/react-spline';
import { useState } from 'react';

export default function SplineBackground() {
    const [isLoaded, setIsLoaded] = useState(false);

    return (
        <div className="fixed inset-0 w-full h-full -z-10 bg-black overflow-hidden pointer-events-none">
            <div
                className={`w-full h-full transition-opacity duration-1000 ${isLoaded ? "opacity-100" : "opacity-0"
                    }`}
            >
                <Spline
                    scene="https://prod.spline.design/UVGJAqLm9u1mRPDP/scene.splinecode"
                    onLoad={() => setIsLoaded(true)}
                />
            </div>
            {/* Decorative gradient overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-80" />
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_transparent_0%,_rgba(0,0,0,0.8)_100%)]" />
        </div>
    );
}
