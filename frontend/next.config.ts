import type { NextConfig } from "next";



const nextConfig:NextConfig = {
  compress:false,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/api/:path*', // Your backend URL
      },
    ];
  },
};



export default nextConfig;
