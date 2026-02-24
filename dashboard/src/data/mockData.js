export const OEE_WATERFALL_DATA = [
    { name: 'Baseline', value: 83.8, type: 'total' },
    { name: 'Availability', value: -6.0, type: 'loss' },
    { name: 'Performance', value: -3.0, type: 'loss' },
    { name: 'Quality', value: -1.4, type: 'loss' },
    { name: 'Current', value: 73.4, type: 'total' },
];

export const OEE_TRENDS = [
    { week: 'W1', availability: 90, performance: 95, quality: 98 },
    { week: 'W2', availability: 89, performance: 94, quality: 98 },
    { week: 'W3', availability: 88, performance: 94, quality: 97 },
    { week: 'W4', availability: 90, performance: 95, quality: 98 },
    { week: 'W5', availability: 86, performance: 93, quality: 96 },
    { week: 'W6', availability: 84, performance: 92, quality: 95 },
    { week: 'W7', availability: 85, performance: 92, quality: 95 },
    { week: 'W8', availability: 84, performance: 92, quality: 95 },
];

export const SCRAP_MARGIN_DATA = [
    { week: 'W1', scrapRate: 3.8, marginImpact: 0 },
    { week: 'W2', scrapRate: 4.1, marginImpact: 3.6 },
    { week: 'W3', scrapRate: 4.4, marginImpact: 7.2 },
    { week: 'W4', scrapRate: 4.8, marginImpact: 14.4 },
    { week: 'W5', scrapRate: 5.7, marginImpact: 21.6 },
    { week: 'W6', scrapRate: 6.5, marginImpact: 29.7 },
    { week: 'W7', scrapRate: 6.2, marginImpact: 26.4 },
    { week: 'W8', scrapRate: 6.0, marginImpact: 24.0 },
];

export const RATE_READINESS_DATA = [
    { id: 1, line: 'Line 3 - Stamping', target: 120, actual: 98, attainment: 81.6, bottleneck: true, status: 'Red' },
    { id: 2, line: 'Line 1 - Assembly', target: 200, actual: 195, attainment: 97.5, bottleneck: false, status: 'Green' },
    { id: 3, line: 'Line 2 - Finishing', target: 150, actual: 142, attainment: 94.7, bottleneck: false, status: 'Yellow' },
    { id: 4, line: 'Packaging A', target: 300, actual: 298, attainment: 99.3, bottleneck: false, status: 'Green' },
    { id: 5, line: 'Quality Inspection', target: 400, actual: 380, attainment: 95.0, bottleneck: false, status: 'Green' },
];

export const ANOMALIES = [
    {
        id: 1,
        timestamp: '2026-02-21 07:45',
        asset: 'Line 3 Stamping Press',
        metric: 'Vibration Index',
        severity: 85,
        rootCause: 'Bearing wear in main drive',
        action: 'Schedule emergency lubrication and vibration re-test.',
        resolved: false
    },
    {
        id: 2,
        timestamp: '2026-02-21 06:12',
        asset: 'Line 1 Glue Station',
        metric: 'Temperature',
        severity: 42,
        rootCause: 'Ambient humidity shift impacting sensor',
        action: 'Recalibrate infrared sensor threshold.',
        resolved: true
    },
    {
        id: 3,
        timestamp: '2026-02-21 04:30',
        asset: 'Line 3 - Quality Output',
        metric: 'Scrap Rate',
        severity: 92,
        rootCause: 'Material feed misalignment',
        action: 'Halt production on Line 3 for alignment audit.',
        resolved: false
    }
];
