'use client';

import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import axios from 'axios';
import SplineBackground from '@/components/SplineBackground';
import VideoLinkInput from '@/components/VideoLinkInput';
import ProgressTracker from '@/components/ProgressTracker';
import SocialPublisher from '@/components/SocialPublisher';

const API_BASE = 'http://localhost:8000/api/v1';

export default function Home() {
  const [activeJobId, setActiveJobId] = useState<string | null>(null);

  // 1. Mutation to submit the video URL
  const submitTask = useMutation({
    mutationFn: async (url: string) => {
      const res = await axios.post(`${API_BASE}/video/process`, { youtube_url: url });
      return res.data; // { job_id: "...", status: "queued" }
    },
    onSuccess: (data) => {
      setActiveJobId(data.job_id);
    }
  });

  // 2. Query to poll the job status if we have an activeJobId
  const { data: jobStatus } = useQuery({
    queryKey: ['jobStatus', activeJobId],
    queryFn: async () => {
      const res = await axios.get(`${API_BASE}/video/jobs/${activeJobId}`);
      return res.data;
    },
    enabled: !!activeJobId,
    refetchInterval: (query) => {
      const data = query.state.data as { status?: string } | undefined;
      return data?.status === 'completed' || data?.status === 'failed' ? false : 2000;
    },
  });

  const isCompleted = jobStatus?.status === 'completed';

  return (
    <main className="relative min-h-screen flex flex-col items-center justify-center p-4 sm:p-8">
      <SplineBackground />

      <div className="z-10 w-full flex flex-col items-center space-y-4">
        <VideoLinkInput
          onSubmit={(url) => submitTask.mutate(url)}
          isLoading={submitTask.isPending}
        />

        {activeJobId && !isCompleted && (
          <ProgressTracker
            status={jobStatus?.status || 'queued'}
            progress={jobStatus?.progress || 0}
            message={jobStatus?.message || 'Connecting to processing server...'}
          />
        )}

        {isCompleted && activeJobId && (
          <SocialPublisher jobId={activeJobId} />
        )}
      </div>
    </main>
  );
}
