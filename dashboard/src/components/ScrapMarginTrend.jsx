import React from 'react';
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ScrapMarginTrend = ({ data }) => {
    return (
        <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid stroke="#f5f5f5" vertical={false} />
                    <XAxis dataKey="week" axisLine={false} tickLine={false} />
                    <YAxis
                        yAxisId="left"
                        orientation="left"
                        stroke="#94a3b8"
                        axisLine={false}
                        tickLine={false}
                        label={{ value: 'Scrap Rate (%)', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fontSize: '10px' } }}
                    />
                    <YAxis
                        yAxisId="right"
                        orientation="right"
                        stroke="#94a3b8"
                        axisLine={false}
                        tickLine={false}
                        label={{ value: 'Margin Impact ($k)', angle: 90, position: 'insideRight', style: { textAnchor: 'middle', fontSize: '10px' } }}
                    />
                    <Tooltip
                        contentStyle={{ fontSize: '12px', borderRadius: '4px', border: '1px solid #e2e8f0' }}
                    />
                    <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                    <Bar yAxisId="right" dataKey="marginImpact" name="Margin Impact ($k)" fill="#1e3a8a" radius={[2, 2, 0, 0]} barSize={30} />
                    <Line yAxisId="left" type="monotone" dataKey="scrapRate" name="Scrap Rate (%)" stroke="#dc2626" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                </ComposedChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ScrapMarginTrend;
