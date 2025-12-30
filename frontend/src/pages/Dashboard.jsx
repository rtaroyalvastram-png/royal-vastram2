import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, TrendingUp, Calendar, Box } from 'lucide-react';
import api from '../api/axios';

const StatsCard = ({ title, value, icon: Icon, color }) => (
    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
        <div className="flex items-center justify-between">
            <div>
                <p className="text-sm font-medium text-gray-500">{title}</p>
                <h3 className="text-2xl font-bold mt-2 text-gray-900">{value}</h3>
            </div>
            <div className={`p-3 rounded-lg ${color}`}>
                <Icon className="w-6 h-6 text-white" />
            </div>
        </div>
    </div>
);

const Dashboard = () => {
    const [stats, setStats] = useState({
        today: 0,
        month: 0,
        year: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const today = new Date();
                const [daily, monthly, yearly] = await Promise.all([
                    api.get(`/bills/filter?day=${today.getDate()}&month=${today.getMonth() + 1}&year=${today.getFullYear()}`),
                    api.get(`/bills/filter?month=${today.getMonth() + 1}&year=${today.getFullYear()}`),
                    api.get(`/bills/filter?year=${today.getFullYear()}`)
                ]);

                const sumTotal = (bills) => bills.data.reduce((acc, curr) => acc + curr.total_amount, 0);

                setStats({
                    today: sumTotal(daily),
                    month: sumTotal(monthly),
                    year: sumTotal(yearly)
                });
            } catch (error) {
                console.error("Failed to fetch stats", error);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Overview</h1>
                    <p className="text-gray-500">Welcome back, here's what's happening today.</p>
                </div>
                <Link
                    to="/create"
                    className="flex items-center gap-2 bg-amber-600 text-white px-4 py-2 rounded-lg hover:bg-amber-700 transition-colors shadow-lg shadow-amber-200"
                >
                    <Plus className="w-5 h-5" />
                    New Bill
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatsCard
                    title="Today's Sales"
                    value={`₹${stats.today.toLocaleString()}`}
                    icon={TrendingUp}
                    color="bg-amber-600 shadow-amber-200"
                />
                <StatsCard
                    title="This Month"
                    value={`₹${stats.month.toLocaleString()}`}
                    icon={Calendar}
                    color="bg-indigo-900 shadow-indigo-200"
                />
                <StatsCard
                    title="This Year"
                    value={`₹${stats.year.toLocaleString()}`}
                    icon={Box}
                    color="bg-emerald-700 shadow-emerald-200"
                />
            </div>

            {/* Quick Actions or Recent Bills could go here */}
        </div>
    );
};

export default Dashboard;
