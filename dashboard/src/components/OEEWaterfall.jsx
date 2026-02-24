import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, LabelList } from 'recharts';

const OEEWaterfall = ({ data }) => {
    // Pre-process data for waterfall
    const processedData = data.reduce((acc, item, index) => {
        const prevEnd = index === 0 ? 0 : acc[index - 1].end;
        let start, end;

        if (item.type === 'total') {
            start = 0;
            end = item.value;
        } else {
            start = prevEnd;
            end = prevEnd + item.value;
        }

        acc.push({
            ...item,
            start,
            end,
            displayValue: [start, end],
            color: item.type === 'total' ? '#1e3a8a' : item.value < 0 ? '#dc2626' : '#16a34a'
        });
        return acc;
    }, []);

    return (
        <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={processedData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} />
                    <YAxis axisLine={false} tickLine={false} domain={[0, 100]} />
                    <Tooltip
                        cursor={{ fill: 'rgba(0,0,0,0.05)' }}
                        content={({ active, payload }) => {
                            if (active && payload && payload.length) {
                                const data = payload[0].payload;
                                return (
                                    <div className="bg-white p-2 border border-slate-200 shadow-sm rounded-sm text-xs">
                                        <p className="font-semibold">{data.name}</p>
                                        <p className="text-slate-600">Value: {data.value}%</p>
                                        <p className="text-slate-600">Current OEE: {data.end.toFixed(1)}%</p>
                                    </div>
                                );
                            }
                            return null;
                        }}
                    />
                    <Bar dataKey="displayValue">
                        {processedData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                        <LabelList
                            dataKey="value"
                            position="top"
                            formatter={(val) => `${val > 0 ? '+' : ''}${val}%`}
                            style={{ fontSize: '10px', fontWeight: 'bold' }}
                        />
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default OEEWaterfall;
