class Program
{
    static void Main()
    {
        string filePath = "data/movies/movies_watched.csv";
        var directorsCount = new Dictionary<string, int>();
        var yearsCount = new Dictionary<string, int>();

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

                    if (values.Length >= 2)
                    {
                        var yearWatched = values[2].Trim();
                        if (yearsCount.ContainsKey(yearWatched))
                        {
                            yearsCount[yearWatched]++;
                        }
                        else
                        {
                            yearsCount[yearWatched] = 1;
                        }
                    }
                }
            }

            Console.WriteLine("Contagem de diretores:");
            foreach (var director in directorsCount.OrderByDescending(d => d.Value))
            {
                Console.WriteLine($"{director.Key}: {director.Value}");
            }

            Console.WriteLine("\nAnos em que mais assisti filmes:");
            foreach (var year in yearsCount.OrderByDescending(y => y.Value))
            {
                Console.WriteLine($"{year.Key}: {year.Value}");
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"Erro ao ler o arquivo: {e.Message}");
        }
    }
}