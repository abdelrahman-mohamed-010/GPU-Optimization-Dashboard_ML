import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Cpu, Server, Zap, Maximize2, TrendingUp, Sliders, AlertTriangle, Clock, BarChart2 } from 'lucide-react';
interface TabButtonProps {
  id: string | number; // assuming id can be a string or number
  label: string;
  icon: React.ReactNode; // assuming icon is a JSX element
}
const GPULoadBalancerDashboard = () => {
  // State for dashboard data
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);
  // Mock data - would be replaced with real data in production
  const [overviewStats, setOverviewStats] = useState<any[]>([
    { name: 'Total GPUs', value: '52,384', icon: <Server size={20} />, color: 'bg-blue-500', trend: '+384 from last week' },
    { name: 'Active Jobs', value: '847', icon: <Activity size={20} />, color: 'bg-green-500', trend: '+12% from yesterday' },
    { name: 'Avg. Utilization', value: '78.4%', icon: <Cpu size={20} />, color: 'bg-purple-500', trend: '+3.2% this week' },
    { name: 'Power Efficiency', value: '+12.3%', icon: <Zap size={20} />, color: 'bg-amber-500', trend: 'Improved 2.1% today' },
  ]);
  
  // Job categories data
  const jobCategories = [
    { name: 'ML Training', count: 342, change: '+15%', avgDuration: '42.3 hours', color: 'bg-indigo-100 border-indigo-500' },
    { name: 'Inference', count: 289, change: '+8%', avgDuration: '3.2 hours', color: 'bg-green-100 border-green-500' },
    { name: 'Rendering', count: 124, change: '-3%', avgDuration: '8.7 hours', color: 'bg-orange-100 border-orange-500' },
    { name: 'HPC', count: 92, change: '+21%', avgDuration: '18.5 hours', color: 'bg-red-100 border-red-500' },
  ];
  
  // Job completion time trends
  const jobCompletionTrends = [
    { day: 'Mon', ml: 100, inference: 30, rendering: 68, hpc: 85 },
    { day: 'Tue', ml: 95, inference: 28, rendering: 62, hpc: 81 },
    { day: 'Wed', ml: 92, inference: 25, rendering: 60, hpc: 80 },
    { day: 'Thu', ml: 88, inference: 22, rendering: 58, hpc: 77 },
    { day: 'Fri', ml: 85, inference: 20, rendering: 55, hpc: 75 },
    { day: 'Sat', ml: 82, inference: 18, rendering: 50, hpc: 73 },
    { day: 'Sun', ml: 80, inference: 16, rendering: 48, hpc: 70 },
  ];
  
  // Cluster health metrics
  const clusterHealth = [
    { name: 'East Datacenter', status: 'Healthy', utilization: 82, temperature: 'Normal', alerts: 0 },
    { name: 'West Datacenter', status: 'Warning', utilization: 93, temperature: 'High', alerts: 2 },
    { name: 'North Datacenter', status: 'Healthy', utilization: 75, temperature: 'Normal', alerts: 0 },
    { name: 'South Datacenter', status: 'Critical', utilization: 96, temperature: 'Critical', alerts: 5 },
  ];

  const utilizationData = [
    { time: '00:00', nvidia: 72, amd: 68, intel: 65 },
    { time: '04:00', nvidia: 65, amd: 62, intel: 59 },
    { time: '08:00', nvidia: 78, amd: 75, intel: 70 },
    { time: '12:00', nvidia: 88, amd: 82, intel: 78 },
    { time: '16:00', nvidia: 92, amd: 85, intel: 80 },
    { time: '20:00', nvidia: 85, amd: 79, intel: 75 },
  ];

  const [gpuDistribution, gpuDistributionAPI] = useState<any[]>([
  
    { name: 'NVIDIA', value: 28500, color: '#76b900' },
    { name: 'AMD', value: 16400, color: '#ED1C24' },
    { name: 'Intel', value: 7484, color: '#0071c5' },
  ]);

  const rlMetricsData = [
    { time: 'Day 1', reward: 120, baseline: 100 },
    { time: 'Day 2', reward: 145, baseline: 105 },
    { time: 'Day 3', reward: 162, baseline: 110 },
    { time: 'Day 4', reward: 170, baseline: 112 },
    { time: 'Day 5', reward: 190, baseline: 115 },
    { time: 'Day 6', reward: 210, baseline: 118 },
    { time: 'Day 7', reward: 235, baseline: 120 },
  ];

  const alerts = [
    { id: 1, severity: 'High', message: 'Thermal throttling detected in Rack B42', time: '14 mins ago' },
    { id: 2, severity: 'Medium', message: 'Job starvation on AMD cluster C12', time: '32 mins ago' },
    { id: 3, severity: 'Low', message: 'Power consumption spike in building East-3', time: '1 hr ago' },
  ];
  interface TabButtonProps {
    id: string | number; // assuming id can be a string or number
    label: string;
    icon: React.ReactNode; // assuming icon is a JSX element
  }
  const TabButton :React.FC<TabButtonProps>= ({ id, label, icon }) => (
    <button
      onClick={() => setActiveTab(id.toString())}
      className={`flex items-center space-x-2 px-4 py-3 text-sm rounded-lg ${
        activeTab === id ? 'bg-blue-100 text-blue-700' : 'hover:bg-gray-100 text-gray-700'
      }`}
    >
      {icon}
      <span>{label}</span>
    </button>
  );


  const fetchOverviewStats = async () => {
    console.log("Call inside");
    setLoading(true);
    try {
      // Replace the URL with the actual endpoint
     const response = await axios.get('http://localhost:8000/overview_stats');
     console.log("Call inside setLoading True", response.data.companies.NVIDIA);

      
      // Assuming the response contains the following fields:
     // const { totalGPUs, activeJobs, avgUtilization, powerEfficiency } = response.data;
      
      // Update the overview stats with the values from the API response
      const mockData = {
        totalGPUs: "55,000",
        activeJobs: "1,200",
        avgUtilization: "80%",
        powerEfficiency: "+15%"
      };
      gpuDistributionAPI([
  
        { name: 'NVIDIA', value: response.data.companies.NVIDIA, color: '#76b900' },
        { name: 'AMD', value: response.data.companies.AMD, color: '#ED1C24' },
        { name: 'Intel', value: response.data.companies.INTEL, color: '#0071c5' },
      ]);
      // Update the overview stats with the values from the API response
      setOverviewStats([
        { name: 'Total GPUs', value: response.data.total_gpus, icon: <Server size={20} />, color: 'bg-blue-500', trend: '+384 from last week' },
        { name: 'Active Jobs', value: mockData.activeJobs, icon: <Activity size={20} />, color: 'bg-green-500', trend: '+12% from yesterday' },
        { name: 'Avg. Utilization', value: response.data.average_utilization+'%', icon: <Cpu size={20} />, color: 'bg-purple-500', trend: '+3.2% this week' },
        { name: 'Power Efficiency', value: response.data.power_efficiency+'%', icon: <Zap size={20} />, color: 'bg-amber-500', trend: 'Improved 2.1% today' },
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchOverviewStats(); // Call fetch function on refresh button click
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="flex justify-between items-center px-6 py-4">
          <div className="flex items-center space-x-2">
            <Maximize2 size={24} className="text-blue-600" />
            <h1 className="text-xl font-bold">GPU Optimizer</h1>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">Last updated: Just now</span>
            <button  onClick={handleRefresh}  className="px-3 py-1 bg-blue-600 text-white rounded-md text-sm">Refresh</button>
          </div>
        </div>
        
        {/* Top-level metrics */}
        <div className="grid grid-cols-4 border-t border-gray-200">
          {overviewStats.map((stat, index) => (
            <div key={index} className="p-3 flex items-center border-r border-gray-200 last:border-r-0">
              <div className={`${stat.color} rounded-full p-2 h-8 w-8 flex items-center justify-center text-white mr-3`}>
                {stat.icon}
              </div>
              <div>
                <p className="text-xs text-gray-500">{stat.name}</p>
                <div className="flex items-center">
                  <p className="text-lg font-semibold mr-2">{stat.value}</p>
                  <p className="text-xs text-gray-500">{stat.trend}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </header>

      <div className="flex h-full">
        {/* Sidebar */}
        <aside className="w-56 bg-white border-r border-gray-200 shadow-sm">
          <nav className="p-4">
            <div className="space-y-1">
              <TabButton id="overview" label="Overview" icon={<BarChart2 size={18} />} />
              <TabButton id="utilization" label="Utilization" icon={<Activity size={18} />} />
              <TabButton id="rl-metrics" label="RL Performance" icon={<TrendingUp size={18} />} />
              <TabButton id="alerts" label="Alerts" icon={<AlertTriangle size={18} />} />
              <TabButton id="settings" label="Settings" icon={<Sliders size={18} />} />
            </div>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold">Cluster Overview</h2>

              {/* Job Category Breakdown */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-base font-medium">Active Jobs by Category</h3>
                  <button className="text-xs text-blue-600 hover:underline">View All Jobs</button>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Count</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Change</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Avg Duration</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Trend</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {jobCategories.map((category, i) => (
                        <tr key={i}>
                          <td className="px-4 py-3 whitespace-nowrap">
                            <div className={`inline-block w-2 h-2 rounded-full mr-2 ${category.color.split(' ')[0]}`}></div>
                            {category.name}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap font-medium">{category.count}</td>
                          <td className={`px-4 py-3 whitespace-nowrap ${category.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                            {category.change}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap">{category.avgDuration}</td>
                          <td className="px-4 py-3 whitespace-nowrap">
                            <div className="w-16 h-6">
                              <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={jobCompletionTrends}>
                                  <Area 
                                    type="monotone" 
                                    dataKey={category.name.toLowerCase().replace(' ', '')} 
                                    stroke={category.color.includes('indigo') ? '#4F46E5' : 
                                           category.color.includes('green') ? '#10B981' : 
                                           category.color.includes('orange') ? '#F97316' : '#EF4444'} 
                                    fill={category.color.includes('indigo') ? '#EEF2FF' : 
                                         category.color.includes('green') ? '#ECFDF5' : 
                                         category.color.includes('orange') ? '#FFF7ED' : '#FEF2F2'} 
                                  />
                                </AreaChart>
                              </ResponsiveContainer>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Charts Row */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* GPU Distribution */}
                <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                  <h3 className="text-base font-medium mb-4">GPU Vendor Distribution</h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={gpuDistribution}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={90}
                          paddingAngle={2}
                          dataKey="value"
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        >
                          {gpuDistribution.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(value) => new Intl.NumberFormat().format(Number(value))} />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* RL Performance */}
                <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                  <h3 className="text-base font-medium mb-4">RL Performance Improvement</h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={rlMetricsData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Area type="monotone" dataKey="reward" stroke="#8884d8" fill="#8884d8" fillOpacity={0.3} />
                        <Area type="monotone" dataKey="baseline" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.3} />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* Job Completion Time Trends */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <h3 className="text-base font-medium mb-4">Job Completion Time Trends (Lower is Better)</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={jobCompletionTrends}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="day" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="ml" name="ML Training" stroke="#4F46E5" strokeWidth={2} />
                      <Line type="monotone" dataKey="inference" name="Inference" stroke="#10B981" strokeWidth={2} />
                      <Line type="monotone" dataKey="rendering" name="Rendering" stroke="#F97316" strokeWidth={2} />
                      <Line type="monotone" dataKey="hpc" name="HPC" stroke="#EF4444" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-2 text-sm text-gray-500 flex justify-between items-center">
                  <span>Normalized values - 100 is baseline from last week</span>
                  <span className="text-green-600 font-medium">All categories showing improvement trend</span>
                </div>
              </div>

              {/* Datacenter Health Status */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-base font-medium">Cluster Health Overview</h3>
                  <span className="text-xs px-2 py-1 bg-red-100 text-red-800 rounded-full">1 Critical Cluster</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {clusterHealth.map((cluster, i) => (
                    <div 
                      key={i} 
                      className={`border-l-4 rounded-lg p-4 ${
                        cluster.status === 'Healthy' ? 'border-green-500 bg-green-50' : 
                        cluster.status === 'Warning' ? 'border-yellow-500 bg-yellow-50' : 
                        'border-red-500 bg-red-50'
                      }`}
                    >
                      <h4 className="font-medium">{cluster.name}</h4>
                      <div className="mt-2 space-y-1">
                        <p className="text-sm flex justify-between">
                          <span className="text-gray-600">Status:</span>
                          <span className={
                            cluster.status === 'Healthy' ? 'text-green-600' : 
                            cluster.status === 'Warning' ? 'text-yellow-600' : 
                            'text-red-600'
                          }>{cluster.status}</span>
                        </p>
                        <p className="text-sm flex justify-between">
                          <span className="text-gray-600">Utilization:</span>
                          <span className={cluster.utilization > 90 ? 'text-red-600 font-medium' : ''}>{cluster.utilization}%</span>
                        </p>
                        <p className="text-sm flex justify-between">
                          <span className="text-gray-600">Temperature:</span>
                          <span className={
                            cluster.temperature === 'Normal' ? 'text-green-600' : 
                            cluster.temperature === 'High' ? 'text-yellow-600' : 
                            'text-red-600'
                          }>{cluster.temperature}</span>
                        </p>
                        <p className="text-sm flex justify-between">
                          <span className="text-gray-600">Alerts:</span>
                          <span className={cluster.alerts > 0 ? 'text-red-600 font-medium' : 'text-green-600'}>
                            {cluster.alerts > 0 ? `${cluster.alerts} active` : 'None'}
                          </span>
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Utilization Tab */}
          {activeTab === 'utilization' && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold">GPU Utilization Analytics</h2>
              
              {/* Utilization Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-green-500 border-t border-r border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500">NVIDIA Avg. Utilization</p>
                      <p className="text-2xl font-semibold mt-1">85.4%</p>
                    </div>
                    <span className="text-green-600 font-medium text-sm">+2.8% This Week</span>
                  </div>
                </div>
                <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-red-500 border-t border-r border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500">AMD Avg. Utilization</p>
                      <p className="text-2xl font-semibold mt-1">75.2%</p>
                    </div>
                    <span className="text-green-600 font-medium text-sm">+3.2% This Week</span>
                  </div>
                </div>
                <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-blue-500 border-t border-r border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500">Intel Avg. Utilization</p>
                      <p className="text-2xl font-semibold mt-1">72.8%</p>
                    </div>
                    <span className="text-green-600 font-medium text-sm">+4.6% This Week</span>
                  </div>
                </div>
              </div>
              
              {/* 24-Hour Utilization Chart */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-base font-medium">24-Hour Utilization by Vendor</h3>
                  <div className="flex space-x-4">
                    <select className="text-sm border border-gray-300 rounded-md px-2 py-1">
                      <option>Last 24 Hours</option>
                      <option>Last 7 Days</option>
                      <option>Last 30 Days</option>
                    </select>
                    <button className="text-sm text-blue-600">Export Data</button>
                  </div>
                </div>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={utilizationData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis unit="%" domain={[40, 100]} />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="nvidia" name="NVIDIA" stroke="#76b900" strokeWidth={2} />
                      <Line type="monotone" dataKey="amd" name="AMD" stroke="#ED1C24" strokeWidth={2} />
                      <Line type="monotone" dataKey="intel" name="Intel" stroke="#0071c5" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-2 flex justify-between text-sm text-gray-600">
                  <span>Peak utilization at 16:00 - 92% (NVIDIA)</span>
                  <span>Lowest utilization at 04:00 - 59% (Intel)</span>
                </div>
              </div>
              
              {/* Utilization Heatmap by Cluster/Rack */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <h3 className="text-base font-medium mb-3">Utilization Heatmap by Datacenter Rack</h3>
                <div className="grid grid-cols-10 gap-1 mb-4">
                  {[...Array(40)].map((_, i) => {
                    const utilValue = 40 + Math.floor(Math.random() * 60);
                    let bgColor = 'bg-green-100';
                    if (utilValue > 90) bgColor = 'bg-red-400';
                    else if (utilValue > 80) bgColor = 'bg-red-300';
                    else if (utilValue > 70) bgColor = 'bg-yellow-300';
                    else if (utilValue > 60) bgColor = 'bg-yellow-200';
                    else if (utilValue > 50) bgColor = 'bg-green-200';
                    
                    return (
                      <div 
                        key={i} 
                        className={`${bgColor} p-2 text-center rounded ${utilValue > 80 ? 'text-white' : 'text-gray-800'}`}
                        title={`Rack ${Math.floor(i / 10) + 1}-${i % 10 + 1}: ${utilValue}% utilized`}
                      >
                        <div className="text-xs font-medium truncate">{`${Math.floor(i / 10) + 1}-${i % 10 + 1}`}</div>
                        <div className="text-xs">{utilValue}%</div>
                      </div>
                    );
                  })}
                </div>
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-green-100 rounded"></div>
                      <span className="text-xs">40-60%</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-green-200 rounded"></div>
                      <span className="text-xs">60-70%</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-yellow-200 rounded"></div>
                      <span className="text-xs">70-80%</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-yellow-300 rounded"></div>
                      <span className="text-xs">80-90%</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-red-300 rounded"></div>
                      <span className="text-xs">90-95%</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-red-400 rounded"></div>
                      <span className="text-xs">95%+</span>
                    </div>
                  </div>
                  <span className="text-red-600 font-medium">8 racks above 90% utilization</span>
                </div>
              </div>
              
              {/* Underutilized Resources */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-base font-medium">Underutilized Resources</h3>
                  <button className="text-sm text-blue-600">Schedule Rebalancing</button>
                </div>
                <table className="min-w-full">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Rack ID</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">GPU Type</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Utilization</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Duration</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Potential Jobs</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    <tr>
                      <td className="px-4 py-3">East-A12</td>
                      <td className="px-4 py-3">NVIDIA A100</td>
                      <td className="px-4 py-3 text-amber-600">45.2%</td>
                      <td className="px-4 py-3">4+ hours</td>
                      <td className="px-4 py-3">ML Training (3)</td>
                      <td className="px-4 py-3"><button className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">Rebalance</button></td>
                    </tr>
                    <tr>
                      <td className="px-4 py-3">West-B08</td>
                      <td className="px-4 py-3">AMD MI250</td>
                      <td className="px-4 py-3 text-red-600">32.8%</td>
                      <td className="px-4 py-3">6+ hours</td>
                      <td className="px-4 py-3">Rendering (5)</td>
                      <td className="px-4 py-3"><button className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">Rebalance</button></td>
                    </tr>
                    <tr>
                      <td className="px-4 py-3">North-C04</td>
                      <td className="px-4 py-3">Intel Max Series</td>
                      <td className="px-4 py-3 text-amber-600">48.7%</td>
                      <td className="px-4 py-3">2+ hours</td>
                      <td className="px-4 py-3">Inference (7)</td>
                      <td className="px-4 py-3"><button className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">Rebalance</button></td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              {/* Memory Utilization by Vendor */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <h3 className="text-base font-medium mb-4">Memory Utilization by Vendor</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <h4 className="text-sm font-medium mb-2 text-gray-600">NVIDIA</h4>
                    <div className="h-6 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-green-500 rounded-full" style={{ width: '82%' }}></div>
                    </div>
                    <div className="flex justify-between mt-1 text-xs text-gray-600">
                      <span>Used: 1.23 PB (82%)</span>
                      <span>Free: 270 TB</span>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium mb-2 text-gray-600">AMD</h4>
                    <div className="h-6 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-red-500 rounded-full" style={{ width: '74%' }}></div>
                    </div>
                    <div className="flex justify-between mt-1 text-xs text-gray-600">
                      <span>Used: 645 TB (74%)</span>
                      <span>Free: 226 TB</span>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium mb-2 text-gray-600">Intel</h4>
                    <div className="h-6 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-500 rounded-full" style={{ width: '68%' }}></div>
                    </div>
                    <div className="flex justify-between mt-1 text-xs text-gray-600">
                      <span>Used: 306 TB (68%)</span>
                      <span>Free: 144 TB</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* RL Metrics Tab */}
          {activeTab === 'rl-metrics' && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold">Reinforcement Learning Performance</h2>
              
              {/* RL Performance Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                  <p className="text-sm text-gray-500">Avg. Reward Improvement</p>
                  <p className="text-2xl font-semibold mt-1 text-purple-600">+35.2%</p>
                  <p className="text-xs text-gray-500 mt-1">vs. heuristic-only baseline</p>
                </div>
                <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                  <p className="text-sm text-gray-500">Job Throughput Gain</p>
                  <p className="text-2xl font-semibold mt-1 text-green-600">+28.7%</p>
                  <p className="text-xs text-gray-500 mt-1">+164 jobs per day</p>
                </div>
                <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                  <p className="text-sm text-gray-500">Completion Time Reduction</p>
                  <p className="text-2xl font-semibold mt-1 text-blue-600">-22.4%</p>
                  <p className="text-xs text-gray-500 mt-1">Avg. 42.6 min faster per job</p>
                </div>
                <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                  <p className="text-sm text-gray-500">Power Efficiency Gain</p>
                  <p className="text-2xl font-semibold mt-1 text-amber-600">+18.3%</p>
                  <p className="text-xs text-gray-500 mt-1">-12.4 kWh per 100 jobs</p>
                </div>
              </div>
              
              {/* Reward vs Baseline Trend */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-base font-medium">Reward Improvement Over Time</h3>
                  <div className="flex space-x-4">
                    <select className="text-sm border border-gray-300 rounded-md px-2 py-1">
                      <option>Last 7 Days</option>
                      <option>Last 30 Days</option>
                      <option>Last Quarter</option>
                    </select>
                    <button className="text-sm text-blue-600">Export Data</button>
                  </div>
                </div>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={rlMetricsData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`${Number(value).toFixed(1)}`, 'Score']} />
                      <Legend />
                      <Bar dataKey="reward" name="RL Model (PPO)" fill="#8884d8" />
                      <Bar dataKey="baseline" name="Heuristic Only" fill="#82ca9d" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-2 flex justify-between text-sm text-gray-600">
                  <span>Model training events: Days 2, 5</span>
                  <span className="text-purple-600 font-medium">Total improvement: +95.8% since Day 1</span>
                </div>
              </div>
              
              {/* Job Type Performance */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Job Completion Improvement */}
                <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                  <h3 className="text-base font-medium mb-4">Completion Time by Job Type</h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart 
                        layout="vertical"
                        data={[
                          { name: 'ML Training', before: 100, after: 72 },
                          { name: 'Inference', before: 100, after: 65 },
                          { name: 'Rendering', before: 100, after: 78 },
                          { name: 'HPC', before: 100, after: 84 }
                        ]}
                        margin={{ left: 80 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" domain={[0, 100]} />
                        <YAxis type="category" dataKey="name" />
                        <Tooltip formatter={(value) => [`${value}%`, 'Relative Time']} />
                        <Legend />
                        <Bar dataKey="before" name="Before RL" fill="#d1d5db" />
                        <Bar dataKey="after" name="With RL" fill="#8884d8" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">Values normalized to pre-RL baseline (100%)</p>
                </div>
                
                {/* Resource Allocation Efficiency */}
                <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                  <h3 className="text-base font-medium mb-4">Resource Allocation Efficiency</h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart 
                        data={[
                          { name: 'NVIDIA', before: 68, after: 85 },
                          { name: 'AMD', before: 62, after: 78 },
                          { name: 'Intel', before: 56, after: 72 }
                        ]}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis unit="%" />
                        <Tooltip formatter={(value) => [`${value}%`, 'Utilization']} />
                        <Legend />
                        <Bar dataKey="before" name="Before RL" fill="#d1d5db" />
                        <Bar dataKey="after" name="With RL" fill="#10b981" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
              
              {/* RL Model Insights */}
              <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <h3 className="text-base font-medium mb-4">Model Performance Insights</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="text-sm font-medium mb-2">Top Reward-Generating Actions</h4>
                    <table className="min-w-full text-sm">
                      <thead>
                        <tr className="bg-gray-50">
                          <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Action Type</th>
                          <th className="px-3 py-2 text-right text-xs font-medium text-gray-500">Avg. Reward</th>
                          <th className="px-3 py-2 text-right text-xs font-medium text-gray-500">Frequency</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        <tr>
                          <td className="px-3 py-2">Inference job batching</td>
                          <td className="px-3 py-2 text-right">+18.3</td>
                          <td className="px-3 py-2 text-right">42.3%</td>
                        </tr>
                        <tr>
                          <td className="px-3 py-2">ML job preemption</td>
                          <td className="px-3 py-2 text-right">+16.7</td>
                          <td className="px-3 py-2 text-right">14.8%</td>
                        </tr>
                        <tr>
                          <td className="px-3 py-2">Vendor-specific optimization</td>
                          <td className="px-3 py-2 text-right">+12.4</td>
                          <td className="px-3 py-2 text-right">22.6%</td>
                        </tr>
                        <tr>
                          <td className="px-3 py-2">Dynamic power scaling</td>
                          <td className="px-3 py-2 text-right">+9.8</td>
                          <td className="px-3 py-2 text-right">20.3%</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium mb-2">Hyperparameter Performance</h4>
                    <table className="min-w-full text-sm">
                      <thead>
                        <tr className="bg-gray-50">
                          <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Parameter</th>
                          <th className="px-3 py-2 text-right text-xs font-medium text-gray-500">Current Value</th>
                          <th className="px-3 py-2 text-right text-xs font-medium text-gray-500">Impact</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        <tr>
                          <td className="px-3 py-2">Learning rate</td>
                          <td className="px-3 py-2 text-right">0.0035</td>
                          <td className="px-3 py-2 text-right text-green-600">High +</td>
                        </tr>
                        <tr>
                          <td className="px-3 py-2">Discount factor</td>
                          <td className="px-3 py-2 text-right">0.98</td>
                          <td className="px-3 py-2 text-right text-green-600">Medium +</td>
                        </tr>
                        <tr>
                          <td className="px-3 py-2">Entropy coefficient</td>
                          <td className="px-3 py-2 text-right">0.01</td>
                          <td className="px-3 py-2 text-right text-amber-600">Low +</td>
                        </tr>
                        <tr>
                          <td className="px-3 py-2">Clip range</td>
                          <td className="px-3 py-2 text-right">0.2</td>
                          <td className="px-3 py-2 text-right text-green-600">Medium +</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              
              {/* Next Steps and Recommendations */}
              <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-purple-500 border-t border-r border-b border-gray-200">
                <h3 className="text-base font-medium mb-3">AI Recommendations</h3>
                <ul className="space-y-2">
                  <li className="flex items-start">
                    <div className="bg-purple-100 rounded-full p-1 mr-2 mt-0.5">
                      <div className="h-2 w-2 rounded-full bg-purple-600"></div>
                    </div>
                    <span className="text-sm">Increase learning rate to 0.004 to improve convergence speed</span>
                  </li>
                  <li className="flex items-start">
                    <div className="bg-purple-100 rounded-full p-1 mr-2 mt-0.5">
                      <div className="h-2 w-2 rounded-full bg-purple-600"></div>
                    </div>
                    <span className="text-sm">Add ML workload-specific feature engineering to observation space</span>
                  </li>
                  <li className="flex items-start">
                    <div className="bg-purple-100 rounded-full p-1 mr-2 mt-0.5">
                      <div className="h-2 w-2 rounded-full bg-purple-600"></div>
                    </div>
                    <span className="text-sm">Schedule next model training for optimal performance (est. +12% improvement)</span>
                  </li>
                </ul>
                <div className="mt-3 flex justify-end">
                  <button className="px-3 py-1 bg-purple-600 text-white rounded-md text-sm">Apply Recommendations</button>
                </div>
              </div>
            </div>
          )}

          {/* Alerts Tab */}
          {activeTab === 'alerts' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold">System Alerts</h2>
                <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                  {alerts.length} Active
                </span>
              </div>
              
              {/* Alerts List */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                {alerts.map((alert) => (
                  <div 
                    key={alert.id} 
                    className="p-4 border-b border-gray-200 last:border-b-0 flex items-start justify-between"
                  >
                    <div className="flex items-start space-x-3">
                      <div 
                        className={`mt-1 h-3 w-3 rounded-full ${
                          alert.severity === 'High' ? 'bg-red-500' : 
                          alert.severity === 'Medium' ? 'bg-yellow-500' : 'bg-blue-500'
                        }`}
                      />
                      <div>
                        <p className="font-medium">{alert.message}</p>
                        <div className="flex items-center mt-1 text-sm text-gray-500">
                          <Clock size={14} className="mr-1" />
                          <span>{alert.time}</span>
                        </div>
                      </div>
                    </div>
                    <span 
                      className={`text-xs px-2 py-1 rounded-full ${
                        alert.severity === 'High' ? 'bg-red-100 text-red-800' : 
                        alert.severity === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'
                      }`}
                    >
                      {alert.severity}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Settings Tab */}
          {activeTab === 'settings' && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold">Dashboard Settings</h2>
              <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                <p className="text-gray-500 mb-6">Configure dashboard preferences and RL algorithm parameters</p>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Auto-refresh Interval
                    </label>
                    <select className="w-full p-2 border border-gray-300 rounded-md">
                      <option>5 seconds</option>
                      <option>30 seconds</option>
                      <option>1 minute</option>
                      <option>5 minutes</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      RL Learning Rate
                    </label>
                    <input 
                      type="range" 
                      min="0" 
                      max="100" 
                      className="w-full" 
                      defaultValue="25"
                    />
                    <div className="flex justify-between text-xs text-gray-500">
                      <span>0.0001</span>
                      <span>0.01</span>
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Priority Vendors
                    </label>
                    <div className="space-y-2">
                      <div className="flex items-center">
                        <input type="checkbox" className="mr-2" defaultChecked />
                        <span>NVIDIA</span>
                      </div>
                      <div className="flex items-center">
                        <input type="checkbox" className="mr-2" defaultChecked />
                        <span>AMD</span>
                      </div>
                      <div className="flex items-center">
                        <input type="checkbox" className="mr-2" defaultChecked />
                        <span>Intel</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default GPULoadBalancerDashboard