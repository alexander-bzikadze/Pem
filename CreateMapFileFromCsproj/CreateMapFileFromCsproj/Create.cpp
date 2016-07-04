#include <iostream>
#include <fstream>
#include <string>

using namespace std;

string getInformationFromText(string findString, string seacrhFraze, int p)
{
	string output;
	for (int i = 0; i < findString.size() - 3; ++i)
	{
		if (findString[i] == seacrhFraze[0] && findString[i + 1] == seacrhFraze[1]
			&& findString[i + 2] == seacrhFraze[2] && findString[i + 3] == seacrhFraze[3])
		{
			i += p;
			while (findString[i] != '"')
			{
				output += findString[i];
				++i;
			}
		}
	}
	return output;
}

void convertFromCsprojToPem(char *wayTofile)
{
	ifstream file(wayTofile, ios::in);
	if (!file.is_open())
	{
		cout << "File not found" << endl;
		return;
	}
	string projectFileName;
	for (int i = 0; wayTofile[i] != '.'; ++i)
	{
		projectFileName += wayTofile[i];
	}
	string proFileName = projectFileName + ".pem";
	ofstream pemFile(proFileName, ios::out);
	pemFile << "Project_name = " << projectFileName << endl << endl;
	string findString;
	pemFile << "Specification: " << endl;
	int check = 0;
	while (!file.eof())
	{
		getline(file, findString);
		string output;
		if (findString.size() > 10)
		{
			string buf = getInformationFromText(findString, "Refe", 19);
			if (buf != "")
			{
				pemFile << "\t" << buf << endl;
			}
			else
			{
				buf = getInformationFromText(findString, "Comp", 17);
				if (buf != "")
				{
					if (check == 0)
					{
						pemFile << endl << "Source: " << endl;
					}
					pemFile << "\t" << buf << endl;
					++check;
				}
			}
		}
	}
	file.close();
	pemFile.close();
}

void main(int argc, char *argv[])
{
	if (argc > 1)
	{
		convertFromCsprojToPem(argv[1]);
	}
}