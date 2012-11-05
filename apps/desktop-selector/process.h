#ifndef PROCESS_H
#define PROCESS_H

#include <QString>
//#include "shellscripts.h"

//! Execute, test and kill shell processes
/*!
  This class is able to execute shell commands declared in an xml file, through \c ShellScripts class.
  Provides functions to execute one shell command or two pipped shell commands.
  Provides one function to test if a program is running, testing for his process.
  Provides one function to kill a running process.
*/
class Process
{
private:
	//! Saves the state of the string representing a shell command: \c true if it is properly set; \c false otherwise.
    bool com;

	//! Sets the \c com member variable
	/*!
		@param status Sets the status of the string representing a shell command: \c true if it is set; \c false otherwise.
	*/
    void setCom(bool status);

	//! Gets the value of the \c com member variable.
	/*!
		@returns \c true if the string representing a shell command is properly set; \c false otherwise.
	*/
    bool isCommandSet();

	//! ShellScript object to get the string representing a shell command.
	/*!
		@see ShellScripts
	*/
//	ShellScripts shsc;

public:
	/*!
		Sets the \c com member variable to \c false.
	*/
    Process();

	//! Checks if a process is running
	/*!
		Executes the <tt>pstree -U</tt> shell command and checks the result string watching for \c process string.

		@param process The name of the process.
                @returns \c true if the requested process is running; \c false otherwise.
	*/
 //   bool isRunning(QString process);

	//! Kill a running rpcess
	/*!
		Kills a process after testing if it is running, using the \c isRunning function.
		@param processName The name of the process to test.
		@returns \c true if the process has been killed; \c false if the process was not running.
	*/
//    bool kill(QString processName);

	//! Executes a shell process
	/*!
		Executes a shell process defined by \c idCommand and \c idParam.
		@param idCommand The command id, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam The command parameters id, defined as a <tt>static QString</tt> in \c ShellScripts class. The default vaule is <tt>ShellScripts::SS_NO_PARAM</tt>.
		@returns A trimmed \c QString containing the shell output after executing the command.
		@see ShellScripts
	*/
	QString execShellProcess(QString idCommand, QString idParam);

	//! Executes a shell process with a custom param
	/*!
		Executes a shell process defined by \c idCommand with a custom parameter.
		@param idCommand The command id, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param custParam A custom parameter, which is not defined in \c ShellScripts class.
		@returns A trimmed \c QString containing the shell output after executing the command.
		@see ShellScripts
	*/
//	QString execShellProcessCustomParam(QString idCommand, QString custParam);

	//! Executes a shell process returning a <tt>QStringList</tt>.
	/*!
		Executes a shell process defined by \c idCommand and \c idParam. Returns a <tt>QStringList</tt>.
		@param idCommand The command id, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam The command parameters id, defined as a <tt>static QString</tt> in \c ShellScripts class. The default vaule is <tt>ShellScripts::SS_NO_PARAM</tt>.
		@returns A \c QStringList collection of trimmed \c QString containing the shell output after executing the command. The list is build by splitting the resulting \c QString by <tt>"\n"</tt>
		@see ShellScripts
	*/
//	QStringList execShellProcessList(QString idCommand, QString idParam);

	//! Executes two pipped shell process
	/*!
		Executes two pipped shell process defined by its \c idCommand and \c idParam. The pipe is in the form: <tt>idCommand1 idParam1 | idCommand2 idParam2</tt>
		@param idCommand1 The command id of the first command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam1 The command parameters id for the first command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idCommand2 The command id of the second command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam2 The command parameters id for the second command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@returns A trimmed \c QString containing the shell output after executing the command.
		@see ShellScripts
	*/
//	QString execPippedShellProcess(QString idCommand1, QString idParam1, QString idCommand2, QString idParam2);

	//! Executes two pipped shell process returning a <tt>QStringList</tt>.
	/*!
		Executes two pipped shell process defined by its \c idCommand and \c idParam. The pipe is in the form: <tt>idCommand1 idParam1 | idCommand2 idParam2</tt>. Returns a <tt>QStringList</tt>.
		@param idCommand1 The command id of the first command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam1 The command parameters id for the first command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idCommand2 The command id of the second command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam2 The command parameters id for the second command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@returns A \c QStringList collection of trimmed \c QString containing the shell output after executing the command. The list is build by splitting the resulting \c QString by <tt>"\n"</tt>
		@see ShellScripts
	*/
//	QStringList execPippedShellProcessList(QString idCommand1, QString idParam1, QString idCommand2, QString idParam2);

	//! Gets a \c QString representing a shell command.
	/*!
		Gets, through \c ShellScripts class, a \c QString representing a shell command.
		@param idCommand The command id, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam The command parameters id, defined as a <tt>static QString</tt> in \c ShellScripts class. The default vaule is <tt>ShellScripts::SS_NO_PARAM</tt>.
		@returns A \c QString representing the shell command.
		@see ShellScripts
	*/
        QString getShellCommand(QString idCommand, QString idParam);


        QString getCommand(QString idCommand, QString idParam);

	//! Gets a \c QString representing two pipped shell commands.
	/*!
		Gets, through \c ShellScripts class, a \c QString representing two pipped shell commands. The pipe is in the form: <tt>idCommand1 idParam1 | idCommand2 idParam2</tt>. Returns a <tt>QStringList</tt>.
		@param idCommand1 The command id of the first command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam1 The command parameters id for the first command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idCommand2 The command id of the second command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@param idParam2 The command parameters id for the second command, defined as a <tt>static QString</tt> in \c ShellScripts class.
		@returns A \c QString representing the shell command.
		@see ShellScripts
	*/
//	QString getPippedShellCommand(QString idCommand1, QString idParam1, QString idCommand2, QString idParam2);
};

#endif // PROCESS_H
