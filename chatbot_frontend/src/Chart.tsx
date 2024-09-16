import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface ChartData {
  type: string | null;
  count: number;
}

interface ChartComponentProps {
  data: ChartData[];
}

const ChartComponent: React.FC<ChartComponentProps> = ({ data }) => {
  // Prepare data for Recharts
  const chartData = data.map((item) => ({
    name: item.type || 'Unknown', // Use 'Unknown' for null types
    count: item.count
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default ChartComponent;
