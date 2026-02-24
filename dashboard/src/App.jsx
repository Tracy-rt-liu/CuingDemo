import React, { useState } from 'react';
import OEEWaterfall from './components/OEEWaterfall';
import ScrapMarginTrend from './components/ScrapMarginTrend';
import RateReadiness from './components/RateReadiness';
import AnomalyFeed from './components/AnomalyFeed';
import {
  OEE_WATERFALL_DATA,
  OEE_TRENDS,
  SCRAP_MARGIN_DATA,
  RATE_READINESS_DATA,
  ANOMALIES
} from './data/mockData';
import {
  LayoutDashboard,
  Filter,
  Download,
  RefreshCcw,
  ChevronDown,
  Factory,
  BarChart3,
  AlertOctagon,
  Settings,
  Bell
} from 'lucide-react';

function App() {
  const [plant, setPlant] = useState('South Carolina - Plant 2');
  const [line, setLine] = useState('All Lines');

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-[1600px] mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-900 p-2 rounded-sm text-white">
              <Factory size={20} />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight">Cuing Analytics</h1>
              <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest leading-none">Enterprise Manufacturing Platform</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-1 px-3 py-1.5 bg-slate-100 rounded-sm text-xs font-semibold text-slate-600 border border-slate-200">
              <RefreshCcw size={14} />
              <span>Synced with SAP: 4m ago</span>
            </div>
            <button className="p-2 text-slate-400 hover:text-slate-600">
              <Settings size={20} />
            </button>
            <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-600 text-xs">
              TL
            </div>
          </div>
        </div>
      </header>

      {/* Control Bar (Filters) */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-[1600px] mx-auto px-6 py-3 flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Plant</span>
              <button className="flex items-center gap-2 px-3 py-1.5 border border-slate-200 rounded-sm text-sm font-medium hover:bg-slate-50 transition-colors">
                {plant} <ChevronDown size={14} />
              </button>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Line</span>
              <button className="flex items-center gap-2 px-3 py-1.5 border border-slate-200 rounded-sm text-sm font-medium hover:bg-slate-50 transition-colors">
                {line} <ChevronDown size={14} />
              </button>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Time Range</span>
              <button className="flex items-center gap-2 px-3 py-1.5 border border-slate-200 rounded-sm text-sm font-medium hover:bg-slate-50 transition-colors">
                Last 8 Weeks <ChevronDown size={14} />
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button className="flex items-center gap-2 px-4 py-1.5 bg-white border border-slate-200 rounded-sm text-sm font-bold text-slate-600 hover:bg-slate-50 transition-colors shadow-sm">
              <Download size={16} /> Export PDF
            </button>
            <button className="flex items-center gap-2 px-4 py-1.5 bg-blue-900 border border-blue-950 rounded-sm text-sm font-bold text-white hover:bg-blue-800 transition-colors shadow-sm">
              <Filter size={16} /> Advanced Filters
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-[1600px] mx-auto p-6">
        <div className="grid grid-cols-12 gap-6">

          {/* Dashboard Body (Left 9 columns) */}
          <div className="col-span-12 lg:col-span-9 space-y-6">

            {/* Top Row: OEE & Scrap */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white border border-slate-200 p-5 rounded-sm shadow-sm">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                      <BarChart3 className="text-blue-700" size={18} />
                      OEE Waterfall (Week-over-Week)
                    </h3>
                    <p className="text-[11px] text-slate-500 font-medium">Diagnostic breakdown of OEE loss across A, P, Q components</p>
                  </div>
                  <span className="text-xs font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded">-12.4% vs Avg</span>
                </div>
                <OEEWaterfall data={OEE_WATERFALL_DATA} />
              </div>

              <div className="bg-white border border-slate-200 p-5 rounded-sm shadow-sm">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                      <AlertOctagon className="text-red-600" size={18} />
                      Scrap & Margin Impact Trend
                    </h3>
                    <p className="text-[11px] text-slate-500 font-medium">Correlation between scrap rate spikes and annualized margin erosion</p>
                  </div>
                  <span className="text-xs font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded">Critical Trend</span>
                </div>
                <ScrapMarginTrend data={SCRAP_MARGIN_DATA} />
              </div>
            </div>

            {/* Middle Row: Rate Readiness */}
            <div className="bg-white border border-slate-200 rounded-sm shadow-sm">
              <div className="p-5 border-b border-slate-200 flex justify-between items-center">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Rate Readiness Report</h3>
                  <p className="text-[11px] text-slate-500 font-medium">Asset-level attainment vs theoretical nameplate capacity</p>
                </div>
                <div className="bg-blue-50 text-blue-700 px-3 py-1 rounded text-[11px] font-bold">
                  AI INSIGHT: Line 3 is structurally capacity-constrained
                </div>
              </div>
              <RateReadiness data={RATE_READINESS_DATA} />
              <div className="p-4 bg-slate-50 rounded-b-sm border-t border-slate-200">
                <p className="text-xs text-slate-600 leading-relaxed italic">
                  <span className="font-bold text-blue-800 uppercase text-[10px] tracking-widest not-italic mr-2">McKinsey Optimization Engine:</span>
                  Current analysis suggests a 4.2% nameplate rate gap on Line 3 due to micro-stoppages. Targeted SMED workshops recommended to reduce changeover drag by 15min.
                </p>
              </div>
            </div>
          </div>

          {/* Anomaly Sidebar (Right 3 columns) */}
          <div className="col-span-12 lg:col-span-3">
            <div className="bg-white border border-slate-200 rounded-sm shadow-sm h-full flex flex-col">
              <div className="p-5 border-b border-slate-200 flex items-center justify-between">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <Bell className="text-blue-700" size={18} />
                  AI Anomaly Feed
                </h3>
                <span className="bg-blue-900 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">2 NEW</span>
              </div>
              <div className="p-6 overflow-y-auto">
                <AnomalyFeed anomalies={ANOMALIES} />
              </div>
              <div className="mt-auto p-4 border-t border-slate-200">
                <button className="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-sm transition-colors">
                  View Full Audit Log
                </button>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}

export default App;
