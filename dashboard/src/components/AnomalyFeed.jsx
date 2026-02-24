import React from 'react';
import { Bell, ShieldAlert, CheckCircle, Info } from 'lucide-react';

const AnomalyFeed = ({ anomalies }) => {
    return (
        <div className="space-y-4">
            {anomalies.map((anomaly) => (
                <div
                    key={anomaly.id}
                    className={`p-4 border rounded-sm relative transition-all ${anomaly.resolved ? 'bg-slate-50 border-slate-200 opacity-60' : 'bg-white border-slate-200 shadow-sm'
                        }`}
                >
                    <div className="flex justify-between items-start mb-2">
                        <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">
                            {anomaly.timestamp}
                        </span>
                        <div className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${anomaly.severity > 80 ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                            }`}>
                            Score: {anomaly.severity}
                        </div>
                    </div>

                    <h4 className="text-sm font-bold text-slate-900 mb-1">{anomaly.asset}</h4>
                    <p className="text-xs text-slate-600 mb-3"><span className="font-semibold">Metric:</span> {anomaly.metric}</p>

                    {!anomaly.resolved && (
                        <div className="bg-amber-50 border-l-2 border-amber-400 p-2 mb-3">
                            <p className="text-[11px] text-amber-800 leading-tight">
                                <span className="font-bold">Hypothesis:</span> {anomaly.rootCause}
                            </p>
                        </div>
                    )}

                    <div className="flex items-center justify-between mt-4">
                        <button className="text-[11px] font-bold text-blue-700 hover:underline">
                            Investigate
                        </button>
                        <button className={`px-3 py-1 rounded text-[11px] font-bold border ${anomaly.resolved
                                ? 'border-slate-300 text-slate-500 bg-slate-100 cursor-not-allowed'
                                : 'border-blue-700 text-blue-700 hover:bg-blue-50'
                            }`}>
                            {anomaly.resolved ? 'Resolved' : 'Mark Resolved'}
                        </button>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default AnomalyFeed;
