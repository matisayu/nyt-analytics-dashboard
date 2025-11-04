import React, { useEffect, useState } from "react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

interface SectionData {
  section: string;
  story_count: number;
}

const API_BASE = import.meta.env.VITE_API_BASE;
console.log("API_BASE:", API_BASE);

function App() {
  const [window, setWindow] = useState<number>(1);
  const [data, setData] = useState<SectionData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchData = async (selectedWindow: number) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/sections/${selectedWindow}`);
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("Error fetching data:", err);
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(window);
  }, [window]);

  const windows = [1, 7, 30];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <h1 className="text-2xl font-bold text-center">NYT Popular Sections</h1>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="1" onValueChange={(v) => setWindow(Number(v))}>
            <TabsList className="flex justify-center mb-4">
              {windows.map((w) => (
                <TabsTrigger key={w} value={w.toString()}>
                  Last {w} Day{w > 1 ? "s" : ""}
                </TabsTrigger>
              ))}
            </TabsList>

            {windows.map((w) => (
              <TabsContent key={w} value={w.toString()}>
                {loading && window === w ? (
                  <p className="text-center text-gray-500">Loading...</p>
                ) : (
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart
                      data={window === w ? data : []}
                      margin={{ top: 10, right: 30, left: 0, bottom: 30 }}
                    >
                      <XAxis dataKey="section" angle={-30} textAnchor="end" height={70} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="story_count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </TabsContent>
            ))}
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}

export default App;
