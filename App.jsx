import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Activity, Cpu, DollarSign, Zap, TrendingUp, Settings, Play, Pause, BarChart3 } from 'lucide-react'
import './App.css'

function App() {
  const [isRunning, setIsRunning] = useState(false)
  const [currentCoin, setCurrentCoin] = useState('BTC')
  const [miningData, setMiningData] = useState({
    dailyProfit: 12.45,
    hashRate: '50 TH/s',
    temperature: 65,
    powerConsumption: 250,
    efficiency: 85,
    uptime: '24h 15m'
  })

  const [cryptoPrices, setCryptoPrices] = useState({
    BTC: { price: 60000, change: 2.5 },
    ETH: { price: 3000, change: -1.2 },
    LTC: { price: 150, change: 0.8 }
  })

  const toggleMining = () => {
    setIsRunning(!isRunning)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              بوت التعدين الذكي
            </h1>
            <p className="text-slate-400 mt-2">نظام تعدين ذكي مدعوم بالذكاء الاصطناعي</p>
          </div>
          <div className="flex items-center gap-4">
            <Badge variant={isRunning ? "default" : "secondary"} className="px-4 py-2">
              {isRunning ? "يعمل" : "متوقف"}
            </Badge>
            <Button 
              onClick={toggleMining}
              className={`px-6 py-2 ${isRunning ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'}`}
            >
              {isRunning ? <Pause className="w-4 h-4 mr-2" /> : <Play className="w-4 h-4 mr-2" />}
              {isRunning ? "إيقاف" : "تشغيل"}
            </Button>
          </div>
        </div>

        {/* Main Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-300">الربح اليومي</CardTitle>
              <DollarSign className="h-4 w-4 text-green-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-400">${miningData.dailyProfit}</div>
              <p className="text-xs text-slate-400">+12% من الأمس</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-300">معدل الهاش</CardTitle>
              <Cpu className="h-4 w-4 text-blue-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-400">{miningData.hashRate}</div>
              <p className="text-xs text-slate-400">مستقر</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-300">درجة الحرارة</CardTitle>
              <Activity className="h-4 w-4 text-orange-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-400">{miningData.temperature}°C</div>
              <Progress value={miningData.temperature} max={100} className="mt-2" />
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-300">استهلاك الطاقة</CardTitle>
              <Zap className="h-4 w-4 text-yellow-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-400">{miningData.powerConsumption}W</div>
              <p className="text-xs text-slate-400">كفاءة {miningData.efficiency}%</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="dashboard" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-slate-800/50">
            <TabsTrigger value="dashboard">لوحة التحكم</TabsTrigger>
            <TabsTrigger value="mining">التعدين</TabsTrigger>
            <TabsTrigger value="analytics">التحليلات</TabsTrigger>
            <TabsTrigger value="settings">الإعدادات</TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Current Mining Status */}
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Cpu className="w-5 h-5" />
                    حالة التعدين الحالية
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300">العملة المُعدَّنة:</span>
                    <Badge variant="outline" className="text-orange-400 border-orange-400">
                      {currentCoin}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300">وقت التشغيل:</span>
                    <span className="text-green-400">{miningData.uptime}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300">الكفاءة:</span>
                    <div className="flex items-center gap-2">
                      <Progress value={miningData.efficiency} className="w-20" />
                      <span className="text-blue-400">{miningData.efficiency}%</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Crypto Prices */}
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5" />
                    أسعار العملات المشفرة
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {Object.entries(cryptoPrices).map(([coin, data]) => (
                    <div key={coin} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline">{coin}</Badge>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold">${data.price.toLocaleString()}</div>
                        <div className={`text-sm ${data.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {data.change >= 0 ? '+' : ''}{data.change}%
                        </div>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="mining" className="space-y-6">
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle>إعدادات التعدين</CardTitle>
                <CardDescription>
                  تحكم في عمليات التعدين واختر العملة المناسبة
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {Object.keys(cryptoPrices).map((coin) => (
                    <Card 
                      key={coin} 
                      className={`cursor-pointer transition-all ${
                        currentCoin === coin 
                          ? 'bg-blue-600/20 border-blue-400' 
                          : 'bg-slate-700/50 border-slate-600 hover:bg-slate-700'
                      }`}
                      onClick={() => setCurrentCoin(coin)}
                    >
                      <CardContent className="p-4 text-center">
                        <div className="text-lg font-semibold">{coin}</div>
                        <div className="text-sm text-slate-400">
                          ${cryptoPrices[coin].price.toLocaleString()}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  تحليلات الأداء
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12 text-slate-400">
                  <BarChart3 className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>سيتم إضافة الرسوم البيانية والتحليلات قريباً</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="w-5 h-5" />
                  إعدادات البوت
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12 text-slate-400">
                  <Settings className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>سيتم إضافة إعدادات التحكم المتقدمة قريباً</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

