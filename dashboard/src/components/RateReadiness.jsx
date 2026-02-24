import React from 'react';
import { AlertCircle, CheckCircle2, AlertTriangle } from 'lucide-react';

const RateReadiness = ({ data }) => {
    return (
        <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 text-sm">
                <thead className="bg-slate-50">
                    <tr>
                        <th className="px-4 py-3 text-left font-semibold text-slate-700">Line / Asset</th>
                        <th className="px-4 py-3 text-right font-semibold text-slate-700">Target (u/h)</th>
                        <th className="px-4 py-3 text-right font-semibold text-slate-700">Actual (u/h)</th>
                        <th className="px-4 py-3 text-right font-semibold text-slate-700">Attainment</th>
                        <th className="px-4 py-3 text-center font-semibold text-slate-700">Status</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 bg-white">
                    {data.map((item) => (
                        <tr key={item.id} className={item.bottleneck ? 'bg-red-50/50' : ''}>
                            <td className="px-4 py-3 font-medium text-slate-900 flex items-center gap-2">
                                {item.line}
                                {item.bottleneck && <AlertTriangle className="h-4 w-4 text-red-500" />}
                            </td>
                            <td className="px-4 py-3 text-right text-slate-600">{item.target}</td>
                            <td className="px-4 py-3 text-right text-slate-600">{item.actual}</td>
                            <td className="px-4 py-3 text-right font-semibold text-slate-900">{item.attainment}%</td>
                            <td className="px-4 py-3 text-center">
                                <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${item.status === 'Green' ? 'bg-green-100 text-green-800' :
                                        item.status === 'Yellow' ? 'bg-yellow-100 text-yellow-800' :
                                            'bg-red-100 text-red-800'
                                    }`}>
                                    {item.status}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default RateReadiness;
