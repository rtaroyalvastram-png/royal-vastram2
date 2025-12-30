import React, { useState } from 'react';
import { Trash, AlertTriangle, CheckCircle, RefreshCw } from 'lucide-react';
import api from '../api/axios';

const Settings = () => {
    const [modalOpen, setModalOpen] = useState(false);
    const [selectedRetention, setSelectedRetention] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);

    const cleanupOptions = [
        {
            id: 'weekly',
            title: 'Clean Weekly Data',
            description: 'Keep data from the last 7 days. Delete everything older.',
            days: 7,
            color: 'bg-green-50 text-green-700 border-green-200'
        },
        {
            id: 'monthly',
            title: 'Clean Monthly Data',
            description: 'Keep data from the last 30 days. Delete everything older.',
            days: 30,
            color: 'bg-blue-50 text-blue-700 border-blue-200'
        },
        {
            id: 'yearly',
            title: 'Clean Yearly Data',
            description: 'Keep data from the last 365 days. Delete everything older.',
            days: 365,
            color: 'bg-amber-50 text-amber-700 border-amber-200'
        },
        {
            id: 'all',
            title: 'Delete ALL Data',
            description: 'Permanently delete ALL bills and images. Start fresh.',
            days: 0,
            color: 'bg-red-50 text-red-700 border-red-200'
        }
    ];

    const handleCleanupClick = (option) => {
        setSelectedRetention(option);
        setModalOpen(true);
        setMessage(null);
    };

    const confirmCleanup = async () => {
        if (!selectedRetention) return;

        setLoading(true);
        try {
            const response = await api.delete(`/bills/cleanup?retention_days=${selectedRetention.days}`);
            setMessage({
                type: 'success',
                text: response.data.message
            });
        } catch (error) {
            console.error(error);
            setMessage({
                type: 'error',
                text: 'Cleanup failed. Please check the backend connection.'
            });
        } finally {
            setLoading(false);
            setModalOpen(false);
            setSelectedRetention(null);
        }
    };

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Settings</h1>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="p-6 border-b border-gray-100">
                    <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                        <Trash className="w-5 h-5 text-red-500" />
                        Database Management
                    </h2>
                    <p className="text-gray-500 text-sm mt-1">
                        Manage your data storage. Use these options to remove old bills and images to free up space.
                    </p>
                </div>

                <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
                    {cleanupOptions.map((option) => (
                        <div
                            key={option.id}
                            className={`p-6 rounded-xl border ${option.color} hover:shadow-md transition-shadow cursor-pointer`}
                            onClick={() => handleCleanupClick(option)}
                        >
                            <div className="flex justify-between items-start mb-4">
                                <div className={`p-2 rounded-lg bg-white bg-opacity-60`}>
                                    <RefreshCw className="w-6 h-6" />
                                </div>
                            </div>
                            <h3 className="font-bold text-lg mb-2">{option.title}</h3>
                            <p className="text-sm opacity-90">{option.description}</p>
                        </div>
                    ))}
                </div>

                {/* Status Message */}
                {message && (
                    <div className={`mx-6 mb-6 p-4 rounded-lg flex items-center gap-3 ${message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                        {message.type === 'success' ? <CheckCircle className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
                        <p>{message.text}</p>
                    </div>
                )}
            </div>

            {/* Confirmation Modal */}
            {modalOpen && selectedRetention && (
                <div className="fixed inset-0 flex items-center justify-center p-4 z-50 py-10" style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
                    <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6 animate-in fade-in zoom-in duration-200">
                        <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-4">
                            <AlertTriangle className="h-8 w-8 text-red-600" />
                        </div>
                        <h3 className="text-xl font-bold text-center text-gray-900 mb-2">Confirm Data Deletion</h3>

                        <p className="text-center text-gray-600 mb-6">
                            Are you sure you want to run <strong>{selectedRetention.title}</strong>?
                            <br /><br />
                            This will <strong>permanently delete</strong> all bills and invoice images older than {selectedRetention.days} days.
                            <br />
                            <span className="text-red-500 font-semibold">This action cannot be undone.</span>
                        </p>

                        <div className="grid grid-cols-2 gap-4">
                            <button
                                onClick={() => setModalOpen(false)}
                                className="px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-bold transition-colors"
                                disabled={loading}
                            >
                                Cancel
                            </button>
                            <button
                                onClick={confirmCleanup}
                                className="px-4 py-3 rounded-lg font-bold shadow-md transition-colors border border-red-700"
                                style={{ backgroundColor: '#DC2626', color: '#FFFFFF' }}
                                disabled={loading}
                            >
                                {loading ? 'Cleaning...' : 'Yes, Delete'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Settings;
