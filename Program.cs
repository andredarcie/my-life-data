class Program
{
    static void Main()
    {
        string filePath = "data/movies/movies_watched.csv";
        var directorsCount = new Dictionary<string, int>();

        try
        {
            using (var reader = new StreamReader(filePath))
            {
                var headerLine = reader.ReadLine();

                while (!reader.EndOfStream)
                {
                    var line = reader.ReadLine();

                    if (line is null) continue;

                    var values = line.Split(',');

                    if (values.Length >= 4)
                    {
                        var director = values[3].Trim();
                        if (directorsCount.ContainsKey(director))
                        {
                            directorsCount[director]++;
                        }
                        else
                        {
                            directorsCount[director] = 1;
                        }
                    }
                }
            }

            foreach (var director in directorsCount.OrderByDescending(d => d.Value))
            {
                Console.WriteLine($"{director.Key}: {director.Value}");
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"Erro ao ler o arquivo: {e.Message}");
        }
    }
}