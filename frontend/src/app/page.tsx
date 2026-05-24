"use client";

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Shield, Zap, Coins, Server, Activity, ArrowRight } from 'lucide-react';

const mockData = [
  { time: '10:00', requests: 120, latency: 240 },
  { time: '10:05', requests: 150, latency: 250 },
  { time: '10:10', requests: 380, latency: 400 },
  { time: '10:15', requests: 210, latency: 260 },
  { time: '10:20', requests: 190, latency: 245 },
  { time: '10:25', requests: 450, latency: 450 },
  { time: '10:30', requests: 320, latency: 310 },
];

export default function Dashboard() {
  return (
    <div className="min-h-screen p-8 font-sans selection:bg-indigo-500/30">
      {/* Header */}
      <header className="flex justify-between items-center mb-12 border-b border-white/10 pb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
            Aegis AI Runtime
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 text-sm font-medium">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            System Operational
          </div>
        </div>
      </header>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard 
          title="Total Requests" 
          value="124.5K" 
          trend="+12%" 
          icon={<Activity className="text-blue-400" />} 
          color="blue"
        />
        <MetricCard 
          title="Tokens Saved (Cache)" 
          value="42.8M" 
          trend="+24%" 
          icon={<Zap className="text-yellow-400" />} 
          color="yellow"
        />
        <MetricCard 
          title="Avg Latency" 
          value="245ms" 
          trend="-15ms" 
          icon={<Server className="text-emerald-400" />} 
          color="emerald"
        />
        <MetricCard 
          title="Cost Prevented" 
          value="$1,240" 
          trend="+8%" 
          icon={<Coins className="text-purple-400" />} 
          color="purple"
        />
      </div>

      {/* Charts & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl shadow-2xl">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-semibold text-gray-200">Traffic & Latency</h2>
            <select className="bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-gray-300 outline-none focus:ring-2 focus:ring-indigo-500/50">
              <option>Last 1 Hour</option>
              <option>Last 24 Hours</option>
              <option>Last 7 Days</option>
            </select>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                <XAxis dataKey="time" stroke="rgba(255,255,255,0.5)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgba(255,255,255,0.5)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(15,23,42,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Line type="monotone" dataKey="requests" stroke="#818cf8" strokeWidth={3} dot={false} activeDot={{ r: 6, fill: '#818cf8' }} />
                <Line type="monotone" dataKey="latency" stroke="#34d399" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl shadow-2xl flex flex-col">
          <h2 className="text-lg font-semibold text-gray-200 mb-6">Recent Invocations</h2>
          <div className="flex-1 overflow-y-auto pr-2 space-y-4">
            <InvocationRow status="success" model="gpt-4o" latency="412ms" tokens="1,204" />
            <InvocationRow status="cache" model="gpt-3.5" latency="12ms" tokens="840" />
            <InvocationRow status="blocked" model="router" latency="4ms" tokens="0" info="Prompt Injection" />
            <InvocationRow status="cache" model="gpt-3.5" latency="15ms" tokens="150" />
            <InvocationRow status="success" model="claude-3" latency="850ms" tokens="4,102" />
          </div>
          <button className="mt-4 w-full py-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors flex items-center justify-center gap-2 text-sm font-medium text-gray-300">
            View All Logs <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, trend, icon, color }: any) {
  return (
    <div className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl shadow-xl hover:bg-white/[0.07] transition-all cursor-default group">
      <div className="flex justify-between items-start mb-4">
        <div className="p-3 rounded-xl bg-white/5 border border-white/5 group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <div className="text-xs font-semibold px-2 py-1 rounded-full bg-white/10 text-gray-300">
          {trend}
        </div>
      </div>
      <div>
        <h3 className="text-gray-400 text-sm font-medium mb-1">{title}</h3>
        <div className="text-3xl font-bold text-white tracking-tight">{value}</div>
      </div>
    </div>
  );
}

function InvocationRow({ status, model, latency, tokens, info }: any) {
  const getStatusColor = () => {
    switch(status) {
      case 'success': return 'bg-blue-500/20 text-blue-400 border-blue-500/20';
      case 'cache': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/20';
      case 'blocked': return 'bg-red-500/20 text-red-400 border-red-500/20';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/20';
    }
  };

  return (
    <div className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors border border-transparent hover:border-white/5">
      <div className="flex items-center gap-3">
        <div className={`text-[10px] font-bold uppercase px-2 py-1 rounded-md border ${getStatusColor()}`}>
          {status}
        </div>
        <div>
          <div className="text-sm font-medium text-gray-200">{model}</div>
          <div className="text-xs text-gray-500">{info || `${tokens} tokens`}</div>
        </div>
      </div>
      <div className="text-sm font-mono text-gray-400">{latency}</div>
    </div>
  );
}
